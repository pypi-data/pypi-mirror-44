/* $NoKeywords: $ */
/*
//
// Copyright (c) 1993-2012 Robert McNeel & Associates. All rights reserved.
// OpenNURBS, Rhinoceros, and Rhino3D are registered trademarks of Robert
// McNeel & Associates.
//
// THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT EXPRESS OR IMPLIED WARRANTY.
// ALL IMPLIED WARRANTIES OF FITNESS FOR ANY PARTICULAR PURPOSE AND OF
// MERCHANTABILITY ARE HEREBY DISCLAIMED.
//				
// For complete openNURBS copyright information see <http://www.opennurbs.org>.
//
////////////////////////////////////////////////////////////////
*/

#include "opennurbs.h"

#if !defined(ON_COMPILING_OPENNURBS)
// This check is included in all opennurbs source .c and .cpp files to insure
// ON_COMPILING_OPENNURBS is defined when opennurbs source is compiled.
// When opennurbs source is being compiled, ON_COMPILING_OPENNURBS is defined 
// and the opennurbs .h files alter what is declared and how it is declared.
#error ON_COMPILING_OPENNURBS must be defined when compiling opennurbs
#endif


////////////////////////////////////////////////////////////////
//   Class ON_Material
////////////////////////////////////////////////////////////////

ON_OBJECT_IMPLEMENT(ON_Material,ON_ModelComponent,"60B5DBBC-E660-11d3-BFE4-0010830122F0");


const ON_Material* ON_Material::FromModelComponentRef(
  const class ON_ModelComponentReference& model_component_reference,
  const ON_Material* none_return_value
  )
{
  const ON_Material* p = ON_Material::Cast(model_component_reference.ModelComponent());
  return (nullptr != p) ? p : none_return_value;
}

// Default constructor
ON_Material::ON_Material() ON_NOEXCEPT
  : ON_ModelComponent(ON_ModelComponent::Type::RenderMaterial)
{}

ON_Material::ON_Material( const ON_Material& src)
  : ON_ModelComponent(ON_ModelComponent::Type::RenderMaterial,src)
{
  Internal_CopyFrom(src);
}

void ON_Material::Internal_CopyFrom(
  const ON_Material& src
  )
{
#define ON_COPY_SRC(m) m=src.m
  ON_COPY_SRC(m_rdk_material_instance_id);
  ON_COPY_SRC(m_ambient);
  ON_COPY_SRC(m_diffuse);
  ON_COPY_SRC(m_emission);
  ON_COPY_SRC(m_specular);
  ON_COPY_SRC(m_reflection);
  ON_COPY_SRC(m_transparent);
  ON_COPY_SRC(m_bShareable);
  ON_COPY_SRC(m_bDisableLighting);
  ON_COPY_SRC(m_bUseDiffuseTextureAlphaForObjectTransparencyTexture);
  ON_COPY_SRC(m_bFresnelReflections);
  ON_COPY_SRC(m_reflectivity);
  ON_COPY_SRC(m_shine);
  ON_COPY_SRC(m_transparency);
  ON_COPY_SRC(m_reflection_glossiness);
  ON_COPY_SRC(m_refraction_glossiness);
  ON_COPY_SRC(m_index_of_refraction);
  ON_COPY_SRC(m_fresnel_index_of_refraction);
  ON_COPY_SRC(m_textures);
  ON_COPY_SRC(m_material_channel);
  ON_COPY_SRC(m_plugin_id);
#undef ON_COPY_SRC
}

bool ON_Material::IsValid( ON_TextLog* text_log ) const
{
  return true;
}

void
ON_Material::Dump( ON_TextLog& dump ) const
{
  ON_ModelComponent::Dump(dump);
  
  dump.Print("ambient rgb = "); dump.PrintRGB( m_ambient ); dump.Print("\n");
  dump.Print("diffuse rgb = "); dump.PrintRGB( m_diffuse ); dump.Print("\n");
  dump.Print("emmisive rgb = "); dump.PrintRGB( m_emission ); dump.Print("\n");
  dump.Print("specular rgb = "); dump.PrintRGB( m_specular ); dump.Print("\n");
  dump.Print("reflection rgb = "); dump.PrintRGB( m_reflection ); dump.Print("\n");
  dump.Print("transparent rgb = "); dump.PrintRGB( m_transparent ); dump.Print("\n");
  dump.Print("shine = %g%%\n",100.0*m_shine/ON_Material::MaxShine );
  dump.Print("transparency = %g%%\n",100.0*m_transparency);
  dump.Print("reflectivity = %g%%\n",100.0*m_reflectivity);
  dump.Print("index of refraction = %g\n",m_index_of_refraction);

  dump.Print("plug-in id = "); dump.Print(m_plugin_id); dump.Print("\n");
  int i;
  for( i = 0; i < m_textures.Count(); i++ )
  {
    dump.Print("texture[%d]:\n",i);
    dump.PushIndent();
    m_textures[i].Dump(dump);
    dump.PopIndent();
  }
}


ON_UUID ON_Material::MaterialPlugInId() const
{
  return m_plugin_id;
}

void ON_Material::SetMaterialPlugInId(
  ON_UUID plugin_id
  )
{
  if (m_plugin_id != plugin_id)
  {
    m_plugin_id = plugin_id;
    IncrementContentVersionNumber();
  }
}

bool ON_Material::Write( ON_BinaryArchive& archive ) const
{
  if (archive.Archive3dmVersion() < 60)
    return Internal_WriteV5(archive);

  const int major_version = 1;
  const int minor_version = 0;
  if (!archive.BeginWrite3dmChunk(TCODE_ANONYMOUS_CHUNK,major_version,minor_version))
    return false;
  
  bool rc = false;
  for (;;)
  {
    const unsigned int attributes_filter
      = ON_ModelComponent::Attributes::IndexAttribute
      | ON_ModelComponent::Attributes::IdAttribute
      | ON_ModelComponent::Attributes::NameAttribute;
    if ( !WriteModelComponentAttributes(archive,attributes_filter)) break;

    if ( !archive.WriteUuid(m_plugin_id) ) break;

    if ( !archive.WriteColor( m_ambient ) ) break;
    if ( !archive.WriteColor( m_diffuse ) ) break;
    if ( !archive.WriteColor( m_emission ) ) break;
    if ( !archive.WriteColor( m_specular ) ) break;
    if ( !archive.WriteColor( m_reflection ) ) break;
    if ( !archive.WriteColor( m_transparent ) ) break;

    if ( !archive.WriteDouble( m_index_of_refraction ) ) break;
    if ( !archive.WriteDouble( m_reflectivity ) ) break;
    if ( !archive.WriteDouble( m_shine ) ) break;
    if (!archive.WriteDouble(m_transparency)) break;

    // array of textures written in a way that user data persists
    {
      const int textures_major_version = 1;
      const int textures_minor_version = 0;
      if (!archive.BeginWrite3dmChunk(TCODE_ANONYMOUS_CHUNK, textures_major_version, textures_minor_version))
        break;
      bool textures_chunk_rc = false;
      for (;;)
      {
        const unsigned int count = m_textures.Count();
        if (!archive.WriteInt(count))
          break;
        unsigned int i;
        for (i = 0; i < count; i++)
        {
          if (!archive.WriteObject(&m_textures[i]))
            break;
        }
        if (i < count)
          break;
        textures_chunk_rc = true;
        break;
      }
      if (!archive.EndWrite3dmChunk())
        textures_chunk_rc = false;
      if ( !textures_chunk_rc )
        break;
    }

    if ( !archive.WriteArray(m_material_channel) )
      break;
    if ( !archive.WriteBool(m_bShareable) )
      break;
    if ( !archive.WriteBool(m_bDisableLighting))
      break;
    if ( !archive.WriteBool(m_bFresnelReflections))
      break;
    if ( !archive.WriteDouble(m_reflection_glossiness))
      break;
    if ( !archive.WriteDouble(m_refraction_glossiness))
      break;
    if ( !archive.WriteDouble(m_fresnel_index_of_refraction)) 
      break;
    if ( !archive.WriteUuid(m_rdk_material_instance_id))
      break;
    if ( !archive.WriteBool(m_bUseDiffuseTextureAlphaForObjectTransparencyTexture))
      break;

    rc = true;
    break;
  }

  if (!archive.EndWrite3dmChunk())
    rc = false;

  return rc;
}


bool ON_Material::Read( ON_BinaryArchive& archive )
{
  *this = ON_Material::Unset;

  if (archive.Archive3dmVersion() < 60)
    return Internal_ReadV5(archive);
  if (archive.ArchiveOpenNURBSVersion() <  2348833910)
    return Internal_ReadV5(archive);

  bool rc = false;
  int major_version = 0;
  int minor_version = 0;
  if (!archive.BeginRead3dmChunk(TCODE_ANONYMOUS_CHUNK,&major_version,&minor_version))
    return false;
  for (;;)
  {
    if (1 != major_version)
      break;

    if ( !ReadModelComponentAttributes(archive)) break;

    if ( !archive.ReadUuid(m_plugin_id) ) break;

    if ( !archive.ReadColor( m_ambient ) ) break;
    if ( !archive.ReadColor( m_diffuse ) ) break;
    if ( !archive.ReadColor( m_emission ) ) break;
    if ( !archive.ReadColor( m_specular ) ) break;
    if ( !archive.ReadColor( m_reflection ) ) break;
    if ( !archive.ReadColor( m_transparent ) ) break;

    if ( !archive.ReadDouble( &m_index_of_refraction ) ) break;
    if ( !archive.ReadDouble( &m_reflectivity ) ) break;
    if ( !archive.ReadDouble( &m_shine ) ) break;
    if (!archive.ReadDouble(&m_transparency)) break;

    // array of textures read in a way that user data persists
    {
      int textures_major_version = 0;
      int textures_minor_version = 0;
      if (!archive.BeginRead3dmChunk(TCODE_ANONYMOUS_CHUNK, &textures_major_version, &textures_minor_version))
        break;
      bool textures_chunk_rc = false;
      for (;;)
      {
        if (1 != textures_major_version)
          break;

        unsigned int count = 0;
        if ( !archive.ReadInt(&count) )
          break;
        m_textures.SetCount(0);
        m_textures.Reserve(count);
        unsigned int i;
        for (i = 0; i < count; i++)
        {
          if (!archive.ReadObject(m_textures.AppendNew()))
            break;
        }
        if (i < count)
          break;
        textures_chunk_rc = true;
        break;
      }
      if (!archive.EndRead3dmChunk())
        textures_chunk_rc = false;
      if (!textures_chunk_rc)
        break;
    }

    if ( !archive.ReadArray(m_material_channel) )
      break;
    if ( !archive.ReadBool(&m_bShareable) )
      break;
    if ( !archive.ReadBool(&m_bDisableLighting))
      break;
    if ( !archive.ReadBool(&m_bFresnelReflections))
      break;
    if ( !archive.ReadDouble(&m_reflection_glossiness))
      break;
    if ( !archive.ReadDouble(&m_refraction_glossiness))
      break;
    if ( !archive.ReadDouble(&m_fresnel_index_of_refraction)) 
      break;
    if ( !archive.ReadUuid(m_rdk_material_instance_id))
      break;
    if ( !archive.ReadBool(&m_bUseDiffuseTextureAlphaForObjectTransparencyTexture))
      break;

    rc = true; 
    break;
  }
  if (!archive.EndRead3dmChunk())
    rc = false;
  return rc;
}

bool ON_Material::Internal_WriteV5( ON_BinaryArchive& file ) const
{
  bool rc = false;
  if ( file.Archive3dmVersion() <= 3 )
  {
    // V2 or V3 file format
    rc = Internal_WriteV3(file);
  }
  else 
  {
    // V4 file format

    // The chunk version 2.0 prevents old V3 IO code from attempting
    // to read this material
    rc = file.Write3dmChunkVersion(2,0); // never change the 2,0


    // version 1.2 field (20061113*)
    // version 1.3 fields (20100917*)
    // version 1.4 fields 6.0.2013-11-6
    // version 1.5 fields 6.0.2014-05-16 (RDK material instance id)
    // version 1.6 fields 6.0.2014-07-11 (m_bUseDiffuseTextureAlphaForObjectTransparencyTexture)
    const int minor_version = (file.Archive3dmVersion() >= 60) ? 6 : 3;
    if (rc) rc = file.BeginWrite3dmChunk(TCODE_ANONYMOUS_CHUNK,1,minor_version);
    if (rc)
    {
      for(;;)
      {
        if ( rc ) rc = file.WriteUuid(Id());
        if ( rc ) rc = file.Write3dmReferencedComponentIndex(*this);
        if ( rc ) rc = file.WriteString(Name());

        if ( rc ) rc = file.WriteUuid(m_plugin_id);

        if ( rc ) rc = file.WriteColor( m_ambient );
        if ( rc ) rc = file.WriteColor( m_diffuse );
        if ( rc ) rc = file.WriteColor( m_emission );
        if ( rc ) rc = file.WriteColor( m_specular );
        if ( rc ) rc = file.WriteColor( m_reflection );
        if ( rc ) rc = file.WriteColor( m_transparent );

        if ( rc ) rc = file.WriteDouble( m_index_of_refraction );
        if ( rc ) rc = file.WriteDouble( m_reflectivity );
        if ( rc ) rc = file.WriteDouble( m_shine );
        if ( rc ) rc = file.WriteDouble( m_transparency );

        if ( !rc )
          break;

        // array of textures written in a way that user data persists
        rc = file.BeginWrite3dmChunk(TCODE_ANONYMOUS_CHUNK,1,0);
        if (rc)
        {
          int i, count = m_textures.Count();
          rc = file.WriteInt(count);
          for ( i = 0; i < count && rc; i++ )
          {
            rc = file.WriteObject(&m_textures[i]);
          }
          if ( !file.EndWrite3dmChunk() )
            rc = false;
        }

        //version 1.1 field
        ON_wString obsolete_flamingo_library = ON_wString::EmptyString;
        if (rc) rc = file.WriteString(obsolete_flamingo_library);

        // version 1.2 field (20061113)
        if (rc) rc = file.WriteArray(m_material_channel);

        // version 1.3 fields (20100917*)
        rc = file.WriteBool(m_bShareable);
        if (!rc) break;
        rc = file.WriteBool(m_bDisableLighting);
        if (!rc) break;

        if ( minor_version >= 4 )
        {
          rc = file.WriteBool(m_bFresnelReflections);
          if (!rc) break;
          rc = file.WriteDouble(m_reflection_glossiness);
          if (!rc) break;
          rc = file.WriteDouble(m_refraction_glossiness);
          if (!rc) break;
          rc = file.WriteDouble(m_fresnel_index_of_refraction);
          if (!rc) break;
          if (minor_version >= 5)
          {
            rc = file.WriteUuid(m_rdk_material_instance_id);
            if (!rc) break;
          }
          if (minor_version >= 6)
          {
            rc = file.WriteBool(m_bUseDiffuseTextureAlphaForObjectTransparencyTexture);
            if (!rc) break;
          }
        }

        break;
      }
      if (!file.EndWrite3dmChunk() )
        rc = false;
    }
  }

  if (rc && file.Archive3dmVersion() < 60)
  {
    if (RdkMaterialInstanceIdIsNotNil())
    {
      // For V5 files and earlier, we need to save
      // the RDK material instance id as user data.
      // Because ON_RdkMaterialInstanceIdObsoleteUserData.DeleteAfterWrite()
      // returns true, the user data we are attaching here will be deleted
      // after it is written.
      ON_RdkMaterialInstanceIdObsoleteUserData* ud = new ON_RdkMaterialInstanceIdObsoleteUserData();
      ud->m_rdk_material_instance_id = RdkMaterialInstanceId();
      const_cast<ON_Material*>(this)->AttachUserData(ud);
    }
  }

  return rc;
}

bool ON_Material::Internal_ReadV5( ON_BinaryArchive& file )
{
  int major_version = 0;
  int minor_version = 0;
  bool rc = file.Read3dmChunkVersion(&major_version,&minor_version);
  if (rc)
  {
    if ( 1 == major_version )
    {
      rc = Internal_ReadV3(file,minor_version);
    }
    else if ( 2 == major_version )
    {
      // fancy V4 material
      // V4 file format

      // The chunk version 2.0 prevents old V3 IO code from attempting
      // to read this material
      rc = file.BeginRead3dmChunk(TCODE_ANONYMOUS_CHUNK,&major_version,&minor_version);
      if (rc)
      {
        for(;;)
        {
          ON_UUID material_id = Id();
          if ( rc ) rc = file.ReadUuid(material_id);
          if (rc) SetId(material_id);

          int material_index = Index();
          if ( rc ) rc = file.ReadInt(&material_index);
          if (rc) SetIndex(material_index);

          ON_wString material_name;
          if ( rc ) rc = file.ReadString(material_name);
          if (rc) SetName(material_name);

          if ( rc ) rc = file.ReadUuid(m_plugin_id);

          if ( rc ) rc = file.ReadColor( m_ambient );
          if ( rc ) rc = file.ReadColor( m_diffuse );
          if ( rc ) rc = file.ReadColor( m_emission );
          if ( rc ) rc = file.ReadColor( m_specular );
          if ( rc ) rc = file.ReadColor( m_reflection );
          if ( rc ) rc = file.ReadColor( m_transparent );

          if ( rc 
               && file.ArchiveOpenNURBSVersion() < 200912010 
               && 128 == m_transparent.Red() 
               && 128 == m_transparent.Green()
               && 128 == m_transparent.Blue()
               )
          {
            // Prior to 1 Dec 2009 the ON_Material::Defaults() set
            // m_transparent to 128,128,128.  This was the wrong
            // value for the default.  This "hack" is here to 
            // make it appear that the default was always white.
            m_transparent = m_diffuse;
          }

          if ( rc ) rc = file.ReadDouble( &m_index_of_refraction );
          if ( rc ) rc = file.ReadDouble( &m_reflectivity );
          if ( rc ) rc = file.ReadDouble( &m_shine );
          if ( rc ) rc = file.ReadDouble( &m_transparency );

          if ( !rc )
            break;

          // array of textures read in a way that user data persists
          int texmajver = 0;
          int texminver = 0;
          rc = file.BeginRead3dmChunk(TCODE_ANONYMOUS_CHUNK,&texmajver,&texminver);
          if (rc)
          {
            if ( 1 == texmajver )
            {
              int i, count = 0;
              rc = file.ReadInt(&count);
              if (rc) m_textures.Reserve(count);
              for ( i = 0; i < count && rc; i++ )
              {
                int trc = file.ReadObject(m_textures.AppendNew());
                if (trc <= 0)
                {
                  // http://mcneel.myjetbrains.com/youtrack/issue/RH-30204
                  // Part of fixing crash reading corrupt file sem2observe copy.3dm
                  rc = false;
                  m_textures.Remove();
                }
                else if ( trc > 1 )
                  m_textures.Remove();
              }
            }
            if ( !file.EndRead3dmChunk() )
              rc = false;
          }

          if ( rc && minor_version >= 1 )
          {
            ON_wString obsolete_flamingo_library;
            rc = file.ReadString(obsolete_flamingo_library);
            if ( !rc ) break;

            if ( minor_version >= 2 )
            {
              // version 1.2 field (20061113)
              rc = file.ReadArray(m_material_channel);
              if (!rc) break;

              if ( minor_version >= 3 )
              {
                // version 1.3 fields (20100917*)
                rc = file.ReadBool(&m_bShareable);
                if (!rc) break;
                rc = file.ReadBool(&m_bDisableLighting);
                if (!rc) break;
                if ( minor_version >= 4 )
                {
                  rc = file.ReadBool(&m_bFresnelReflections);
                  if (!rc) break;
                  rc = file.ReadDouble(&m_reflection_glossiness);
                  if (!rc) break;
                  rc = file.ReadDouble(&m_refraction_glossiness);
                  if (!rc) break;
                  rc = file.ReadDouble(&m_fresnel_index_of_refraction);
                  if (!rc) break;

                  if (minor_version >= 5)
                  {
                    // version 1.5 field 6.0.2014-05-16
                    rc = file.ReadUuid(m_rdk_material_instance_id);
                    if (!rc) break;
                  }

                  if (minor_version >= 6)
                  {
                    // version 1.6 field 6.0.2014-07-11
                    rc = file.ReadBool(&m_bUseDiffuseTextureAlphaForObjectTransparencyTexture);
                    if (!rc) break;
                  }
                }
              }
            }

          }

          break;
        }
        if (!file.EndRead3dmChunk() )
          rc = false;
      }
    }
  }
  return rc;
}


bool ON_Material::Internal_WriteV3( ON_BinaryArchive& file ) const
{
  int i;
  // V2 and V3 file format

  bool rc = file.Write3dmChunkVersion(1,1);
  if ( rc ) rc = file.WriteColor( m_ambient );
  if ( rc ) rc = file.WriteColor( m_diffuse );
  if ( rc ) rc = file.WriteColor( m_emission );
  if ( rc ) rc = file.WriteColor( m_specular );
  if ( rc ) rc = file.WriteDouble( Shine() );
  if (rc) rc = file.WriteDouble(m_transparency);

  if (rc) rc = file.WriteChar((unsigned char)1); // OBSOLETE // m_casts_shadows
  if (rc) rc = file.WriteChar((unsigned char)1); // OBSOLETE // m_shows_shadows

  if (rc) rc = file.WriteChar((unsigned char)0); // OBSOLETE // m_wire_mode
  if (rc) rc = file.WriteChar((unsigned char)2); // OBSOLETE // m_wire_density

  if (rc) rc = file.WriteColor(ON_Color(0, 0, 0)); // OBSOLETE // m_wire_color

  if (rc)
  {
    // OBSOLETE - line style info never used
    short s = 0;
    if (rc) rc = file.WriteShort(s);
    if (rc) rc = file.WriteShort(s);
    if (rc) rc = file.WriteDouble(0.0);
    if (rc) rc = file.WriteDouble(1.0);
  }

  ON_wString filename;
  int j = 0;
  i = FindTexture(nullptr, ON_Texture::TYPE::bitmap_texture);
  if (i >= 0)
  {
    const ON_Texture& tmap = m_textures[i];
    const ON_wString tmap_filename = tmap.m_image_file_reference.FullPath();
    if (tmap_filename.Length() > 0)
    {
      filename = tmap_filename;
      j = (ON_Texture::MODE::decal_texture == tmap.m_mode) ? 2 : 1;
    }
  }
  // OBSOLETE // if ( rc ) rc = file.WriteString( TextureBitmapFileName() );
  // OBSOLETE // i = TextureMode();
  // OBSOLETE // if ( rc ) rc = file.WriteInt( i );
  // OBSOLETE // if ( rc ) rc = file.WriteInt( m_texture_bitmap_index );
  if (rc) rc = file.WriteString(filename);
  if (rc) rc = file.WriteInt(j);
  if (rc) rc = file.WriteInt(0);

  filename.Destroy();
  j = 0;
  double bump_scale = 1.0;
  i = FindTexture(nullptr, ON_Texture::TYPE::bump_texture);
  if (i >= 0)
  {
    const ON_Texture& tmap = m_textures[i];
    const ON_wString tmap_filename = tmap.m_image_file_reference.FullPath();
    if (tmap_filename.Length() > 0)
    {
      filename = tmap_filename;
      j = (ON_Texture::MODE::decal_texture == tmap.m_mode) ? 2 : 1;
      bump_scale = tmap.m_bump_scale[1];
    }
  }
  // OBSOLETE //if ( rc ) rc = file.WriteString( BumpBitmapFileName() );
  // OBSOLETE //i = BumpMode();
  // OBSOLETE //if ( rc ) rc = file.WriteInt( i );
  // OBSOLETE //if ( rc ) rc = file.WriteInt( m_bump_bitmap_index );
  // OBSOLETE //if ( rc ) rc = file.WriteDouble( m_bump_scale );
  if (rc) rc = file.WriteString(filename);
  if (rc) rc = file.WriteInt(j);
  if (rc) rc = file.WriteInt(0);
  if (rc) rc = file.WriteDouble(bump_scale);

  filename.Destroy();
  j = 0;
  i = FindTexture(nullptr, ON_Texture::TYPE::emap_texture);
  if (i >= 0)
  {
    const ON_Texture& tmap = m_textures[i];
    const ON_wString tmap_filename = tmap.m_image_file_reference.FullPath();
    if (tmap_filename.Length() > 0)
    {
      filename = tmap_filename;
      j = (ON_Texture::MODE::decal_texture == tmap.m_mode) ? 2 : 1;
    }
  }
  // OBSOLETE //if ( rc ) rc = file.WriteString( EmapBitmapFileName() );
  // OBSOLETE //i = EmapMode();
  // OBSOLETE //if ( rc ) rc = file.WriteInt( i );
  // OBSOLETE //if ( rc ) rc = file.WriteInt( m_emap_bitmap_index );
  if (rc) rc = file.WriteString(filename);
  if (rc) rc = file.WriteInt(j);
  if (rc) rc = file.WriteInt(0);

  if (rc) rc = file.Write3dmReferencedComponentIndex(*this);

  if (rc) rc = file.WriteUuid(m_plugin_id);

  const ON_wString obsolete_flamingo_library = ON_wString::EmptyString;
  if (rc) rc = file.WriteString(obsolete_flamingo_library);
  if (rc) rc = file.WriteString(Name());


  // 1.1 fields
  if (rc) rc = file.WriteUuid(Id());
  if (rc) rc = file.WriteColor(m_reflection);
  if (rc) rc = file.WriteColor(m_transparent);
  if (rc) rc = file.WriteDouble(m_index_of_refraction);

  return rc;
}



bool ON_Material::Internal_ReadV3( ON_BinaryArchive& file, int minor_version )
{
  double shine = 0.0, transparency = 0.0;
  int i, j;
  bool rc = true;
  {
    // common to all version 1.x formats
    if ( rc ) rc = file.ReadColor( m_ambient );
    if ( rc ) rc = file.ReadColor( m_diffuse );
    if ( rc ) rc = file.ReadColor( m_emission );
    if ( rc ) rc = file.ReadColor( m_specular );
    if ( rc ) rc = file.ReadDouble( &shine );
    if ( rc ) SetShine(shine);
    if ( rc ) rc = file.ReadDouble( &transparency );
    if ( rc ) SetTransparency(transparency);

    unsigned char obsolete_uc;
    if ( rc ) rc = file.ReadChar( &obsolete_uc ); // m_casts_shadows
    if ( rc ) rc = file.ReadChar( &obsolete_uc ); // m_shows_shadows

    if ( rc ) rc = file.ReadChar( &obsolete_uc ); // m_wire_mode
    if ( rc ) rc = file.ReadChar( &obsolete_uc ); // m_wire_density

    ON_Color obsolete_color;
    if ( rc ) rc = file.ReadColor( obsolete_color ); // m_wire_color

    if (rc)
    {
      // OBSOLETE if ( rc ) rc = file.ReadLineStyle( m_wire_style );
      short s;
      double x;
      if (rc) rc = file.ReadShort(&s);
      if (rc) rc = file.ReadShort(&s);
      if (rc) rc = file.ReadDouble(&x);
      if (rc) rc = file.ReadDouble(&x);
    }

    ON_wString str;

    if ( rc ) rc = file.ReadString( str ); //sTextureBitmapFileName
    i = 0;
    j = 0;
    if ( rc ) rc = file.ReadInt( &i );
    // OBSOLETE // if ( rc ) SetTextureMode( ON::TextureMode(i) );
    if ( rc ) rc = file.ReadInt( &j );//&m_texture_bitmap_index

    if ( rc && !str.IsEmpty() )
    {
      ON_Texture& texture = m_textures[AddTexture(static_cast< const wchar_t* >(str),ON_Texture::TYPE::bitmap_texture)];
      if ( 2 == i )
      {
        texture.m_mode = ON_Texture::MODE::decal_texture;
      }
      else
      {
        texture.m_mode = ON_Texture::MODE::modulate_texture;
      }
    }

    if ( rc ) rc = file.ReadString( str ); // sBumpBitmapFileName
    if ( rc ) rc = file.ReadInt( &i );
   // OBSOLETE // if ( rc ) SetBumpMode( ON::TextureMode(i) );
    if ( rc ) rc = file.ReadInt( &j );//&m_bump_bitmap_index );
    double bump_scale = 0.0;
    if ( rc ) rc = file.ReadDouble( &bump_scale );

    if ( rc && !str.IsEmpty() )
    {
      ON_Texture& texture = m_textures[AddTexture(static_cast< const wchar_t* >(str),ON_Texture::TYPE::bump_texture)];
      if ( 2 == i )
      {
        texture.m_mode = ON_Texture::MODE::decal_texture;
      }
      else
      {
        texture.m_mode = ON_Texture::MODE::modulate_texture;
      }
      texture.m_bump_scale.Set(0.0,bump_scale);
    }

    if ( rc ) rc = file.ReadString( str ); // sEmapBitmapFileName
    if ( rc ) rc = file.ReadInt( &i );
    // OBSOLETE // if ( rc ) SetEmapMode( ON::TextureMode(i) );
    if ( rc ) rc = file.ReadInt( &j ); //&m_emap_bitmap_index;

    if ( rc && !str.IsEmpty() )
    {
      ON_Texture& texture = m_textures[AddTexture(static_cast< const wchar_t* >(str),ON_Texture::TYPE::emap_texture)];
      if ( 2 == i )
      {
        texture.m_mode = ON_Texture::MODE::decal_texture;
      }
      else
      {
        texture.m_mode = ON_Texture::MODE::modulate_texture;
      }
    }

    int material_index = Index();
    if ( rc ) rc = file.ReadInt( &material_index );
    if (rc) SetIndex(material_index);

    if ( rc ) rc = file.ReadUuid( m_plugin_id );

    ON_wString obsolete_flamingo_library;
    if ( rc ) rc = file.ReadString( obsolete_flamingo_library );

    ON_wString material_name;
    if ( rc ) rc = file.ReadString( material_name );
    if (rc) SetName(material_name);

    if ( minor_version >= 1 )
    {
      // 1.1 fields
      ON_UUID material_id = Id();
      if (rc) rc = file.ReadUuid( material_id );
      SetId(material_id);
      if (rc) rc = file.ReadColor( m_reflection);
      if (rc) rc = file.ReadColor( m_transparent);
      if (rc) rc = file.ReadDouble( &m_index_of_refraction );
    }
    else
    {
      // old material needs a valid non-nil id.
      SetId();
    }

  }

  return rc;
}

ON::object_type ON_Material::ObjectType() const
{
   return ON::material_object;
}

int ON_Material::FindTexture( const wchar_t* filename, 
                              ON_Texture::TYPE type,
                              int i0
                              ) const
{
  int i, count = m_textures.Count();
  for (i = ((i0 < 0) ? 0 : (i0+1)); i < count; i++ )
  {
    if (    type != m_textures[i].m_type 
         && type != ON_Texture::TYPE::no_texture_type )
    {
      continue;
    }
    const ON_wString texture_file_name = m_textures[i].m_image_file_reference.FullPath();
    if ( filename && texture_file_name.ComparePath(filename) )
    {
      continue;
    }
    return i;
  }
  return -1;
}

double ON_Material::FresnelReflectionCoefficient(
  double fresnel_index_of_refraction,
  const double N[3],
  const double R[3]
  )
{
  double x,y,z,c,g;

  for(;;)
  {
    x = N[0]-R[0];
    y = N[1]-R[1];
    z = N[2]-R[2];
    c = ON_Length3d(x,y,z);
    if ( !(c > ON_DBL_MIN) )
      break;

    c = (N[0]*x + N[1]*y + N[2]*z)/c; // c = N o (N - R) / |N - R|

    g = fresnel_index_of_refraction*fresnel_index_of_refraction + c*c - 1.0;
    g = (g > 0.0) ? sqrt(g) : 0.0;

    // unsafe (potiential divide by zero, overflow, ...) and inefficient
    // return ( ((g-c)*(g-c))/(2*(g+c)*(g+c)) ) * (1.0f + ( ((c*(g+c)-1.0)*(c*(g+c)-1.0))/((c*(g+c)+1.0)*(c*(g+c)+1.0)) ) );

    x = g+c;
    if ( !(x != 0.0) )
      break; // x is NAN or zero

    z = (g-c)/x; // z = (g-c)/(g+c)
    if ( fabs(z) <= 1.0e-154 )
      return 0.0; // z*z below will be zero or denormalized

    x *= c; // x = c*(g+c)

    y = x + 1.0; // y = c*(g+c) + 1.0
    if ( !(y != 0.0) )
      break; // y is NAN or zero
  
    y = (x - 1.0)/y; // y = (c*(g+c) - 1.0)/(c*(g+c) + 1.0)

    x =  0.5*z*z*(1.0 + y*y);
    if ( !(x == x) )
      break; // x is NAN

    if ( !ON_IS_FINITE(x) )
      break; // x is infinity

    return x; // x is 
  }

  return 1.0; // error occured
}

double  ON_Material::FresnelReflectionCoefficient(
  ON_3dVector N,
  ON_3dVector R
  ) const
{
  return m_bFresnelReflections
    ? ON_Material::FresnelReflectionCoefficient(m_fresnel_index_of_refraction,&N.x,&R.x)
    : 1.0;
}

int ON_Material::FindTexture( ON_UUID texture_id ) const
{
  int i, count = m_textures.Count();
  for (i = 0; i < count; i++ )
  {
    if ( !ON_UuidCompare(&texture_id,&m_textures[i].m_texture_id) )
      return i;
  }
  return -1;
}

int ON_Material::DeleteTexture(const wchar_t* filename,ON_Texture::TYPE type )
{
  int deleted_count = 0;
  int i;

  if ( !filename && type == ON_Texture::TYPE::no_texture_type )
  {
    deleted_count = m_textures.Count();
    m_textures.Destroy();
  }
  else
  {
    for ( i = m_textures.Count()-1; i >= 0; i--)
    {
      if ( type != ON_Texture::TYPE::no_texture_type && type != m_textures[i].m_type )
        continue;
      if ( filename && m_textures[i].m_image_file_reference.FullPath().ComparePath(filename) )
        continue;
      m_textures.Remove(i);
      deleted_count++;
    }
  }
  return deleted_count;
}

int ON_Material::AddTexture( const ON_Texture& tx )
{
  // has to copy user data
  int i = FindTexture( static_cast< const wchar_t* >(tx.m_image_file_reference.FullPath()), tx.m_type );
  if ( i < 0 )
  {
    i = m_textures.Count();
    m_textures.Append(tx);
  }
  else
  {
    m_textures[i] = tx;
  }
  if ( ON_UuidIsNil(m_textures[i].m_texture_id) )
  {
    ON_CreateUuid(m_textures[i].m_texture_id);
  }

  return i;
}


int ON_Material::AddTexture(const wchar_t* filename,ON_Texture::TYPE type)
{
  int ti = FindTexture(nullptr,type);
  if ( ti < 0 )
  {
    ti = m_textures.Count();
    m_textures.AppendNew();
  }
  if (ti >= 0 )
  {
    m_textures[ti].m_image_file_reference.SetFullPath(filename,false);
    m_textures[ti].m_type = type;
    m_textures[ti].m_mode = ON_Texture::MODE::modulate_texture;
    m_textures[ti].m_magfilter = ON_Texture::FILTER::linear_filter;
    ON_CreateUuid(m_textures[ti].m_texture_id);
  }
  return ti;
}

// Shine values are in range 0.0 to ON_Material::GetMaxShine()
double ON_Material::Shine() const
{
  return m_shine;
}

void ON_Material::SetShine( double shine )
{
  if (shine == shine) // NANs fail this test
  {
    if (shine < 0.0)
      m_shine = 0.0;
    else if (shine > ON_Material::MaxShine)
      m_shine = ON_Material::MaxShine;
    else
      m_shine = (float)shine;
  }
}

  // Transparency values are in range 0.0 = opaque to 1.0 = transparent
double ON_Material::Transparency( ) const
{
  return  m_transparency;
}

void ON_Material::SetTransparency( double transparency )
{
  if ( transparency < 0.0 )
    m_transparency = 0.0;
  else if ( transparency > 1.0)
    m_transparency = 1.0;
  else
    m_transparency = transparency;
}

  // Transparency values are in range 0.0 = opaque to 1.0 = transparent
double ON_Material::Reflectivity( ) const
{
  return  m_reflectivity;
}

void ON_Material::SetReflectivity( double reflectivity )
{
  if ( reflectivity < 0.0 )
    m_reflectivity = 0.0;
  else if ( reflectivity > 1.0)
    m_reflectivity = 1.0;
  else
    m_reflectivity = reflectivity;
}

bool operator==( const ON_Material& a, const ON_Material& b )
{
  return (0 == ON_Material::Compare(a,b));
}

bool operator!=( const ON_Material& a, const ON_Material& b )
{
  return (0 != ON_Material::Compare(a,b));
}

static int CompareNans(double a, double b)
{
  if (a == a)
  {
    if (b == b)
    {
      return ( ( a < b ) ? -1 : ((a > b) ? 1 : 0 ) );
    }
    // a is not a NAN, b is a NAN
    return -1; // a < b - NAN's are last
  }
  else if (b == b)
  {
    // a is a NAN, b is not a NAN
    return -1; // b < a - NAN's are last
  }
  return 0; // a and b are both NaNs
}

static int CompareDouble( double a, double b )
{
  return ( ( a < b ) ? -1 : ((a > b) ? 1 : (a==b ? 0 : CompareNans(a,b)) ) );
}

static int CompareXform( const ON_Xform& a, const ON_Xform& b )
{
  int i,j;
  const double* da = &a.m_xform[0][0];
  const double* db = &b.m_xform[0][0];
  i = 16;
  j = 0;
  while ( i-- && !j)
  {
    j = CompareDouble(*da++,*db++);
  }

  return j;
}

int ON_Texture::Compare(const ON_Texture& a, const ON_Texture& b)
{
  int rc = ON_UuidCompare(&a.m_texture_id, &b.m_texture_id);
  while (!rc)
  {
    if (a.m_mapping_channel_id < b.m_mapping_channel_id)
      rc = -1;
    else if (a.m_mapping_channel_id > b.m_mapping_channel_id)
      rc = 1;
    if (rc) break;

    rc = a.m_image_file_reference.FullPath().ComparePath(static_cast< const wchar_t* >(b.m_image_file_reference.FullPath()));
    if (rc) break;

    rc = ((int)(a.m_bOn ? 1 : 0)) - ((int)(b.m_bOn ? 1 : 0));
    if (rc) break;

    rc = ((int)a.m_type) - ((int)b.m_type);
    if (rc) break;

    rc = ((int)a.m_mode) - ((int)b.m_mode);
    if (rc) break;

    rc = ((int)a.m_minfilter) - ((int)b.m_minfilter);
    if (rc) break;

    rc = ((int)a.m_magfilter) - ((int)b.m_magfilter);
    if (rc) break;

    rc = ((int)a.m_wrapu) - ((int)b.m_wrapu);
    if (rc) break;

    rc = ((int)a.m_wrapv) - ((int)b.m_wrapv);
    if (rc) break;

    rc = ((int)a.m_wrapw) - ((int)b.m_wrapw);
    if (rc) break;

    rc = CompareXform(a.m_uvw, b.m_uvw);
    if (rc) break;

    rc = a.m_border_color.Compare(b.m_border_color);
    if (rc) break;

    rc = a.m_transparent_color.Compare(b.m_transparent_color);
    if (rc) break;

    rc = ON_Interval::Compare(a.m_bump_scale, b.m_bump_scale);
    if (rc) break;

    rc = CompareDouble(a.m_blend_constant_A, b.m_blend_constant_A);
    if (rc) break;

    rc = CompareDouble(a.m_blend_A0, b.m_blend_A0);
    if (rc) break;
    rc = CompareDouble(a.m_blend_A1, b.m_blend_A1);
    if (rc) break;
    rc = CompareDouble(a.m_blend_A2, b.m_blend_A2);
    if (rc) break;
    rc = CompareDouble(a.m_blend_A3, b.m_blend_A3);
    if (rc) break;

    rc = CompareDouble(a.m_blend_RGB0, b.m_blend_RGB0);
    if (rc) break;
    rc = CompareDouble(a.m_blend_RGB1, b.m_blend_RGB1);
    if (rc) break;
    rc = CompareDouble(a.m_blend_RGB2, b.m_blend_RGB2);
    if (rc) break;
    rc = CompareDouble(a.m_blend_RGB3, b.m_blend_RGB3);
    if (rc) break;

    break;
  }

  return rc;
}

int ON_Texture::CompareAppearance(const ON_Texture& a, const ON_Texture& b)
{
  int rc = 0;
  while (!rc)
  {
    if (a.m_mapping_channel_id < b.m_mapping_channel_id)
      rc = -1;
    else if (a.m_mapping_channel_id > b.m_mapping_channel_id)
      rc = 1;
    if (rc) break;

    rc = a.m_image_file_reference.FullPath().ComparePath(static_cast< const wchar_t* >(b.m_image_file_reference.FullPath()));
    if (rc) break;

    rc = ((int)(a.m_bOn ? 1 : 0)) - ((int)(b.m_bOn ? 1 : 0));
    if (rc) break;

    rc = ((int)a.m_type) - ((int)b.m_type);
    if (rc) break;

    rc = ((int)a.m_mode) - ((int)b.m_mode);
    if (rc) break;

    rc = ((int)a.m_minfilter) - ((int)b.m_minfilter);
    if (rc) break;

    rc = ((int)a.m_magfilter) - ((int)b.m_magfilter);
    if (rc) break;

    rc = ((int)a.m_wrapu) - ((int)b.m_wrapu);
    if (rc) break;

    rc = ((int)a.m_wrapv) - ((int)b.m_wrapv);
    if (rc) break;

    rc = ((int)a.m_wrapw) - ((int)b.m_wrapw);
    if (rc) break;

    rc = CompareXform(a.m_uvw, b.m_uvw);
    if (rc) break;

    rc = a.m_border_color.Compare(b.m_border_color);
    if (rc) break;

    rc = a.m_transparent_color.Compare(b.m_transparent_color);
    if (rc) break;

    rc = ON_Interval::Compare(a.m_bump_scale, b.m_bump_scale);
    if (rc) break;

    rc = CompareDouble(a.m_blend_constant_A, b.m_blend_constant_A);
    if (rc) break;

    rc = CompareDouble(a.m_blend_A0, b.m_blend_A0);
    if (rc) break;
    rc = CompareDouble(a.m_blend_A1, b.m_blend_A1);
    if (rc) break;
    rc = CompareDouble(a.m_blend_A2, b.m_blend_A2);
    if (rc) break;
    rc = CompareDouble(a.m_blend_A3, b.m_blend_A3);
    if (rc) break;

    rc = CompareDouble(a.m_blend_RGB0, b.m_blend_RGB0);
    if (rc) break;
    rc = CompareDouble(a.m_blend_RGB1, b.m_blend_RGB1);
    if (rc) break;
    rc = CompareDouble(a.m_blend_RGB2, b.m_blend_RGB2);
    if (rc) break;
    rc = CompareDouble(a.m_blend_RGB3, b.m_blend_RGB3);
    if (rc) break;

    break;
  }

  return rc;
}

int ON_Material::Compare( const ON_Material& a, const ON_Material& b )
{
  int rc = CompareNameAndIds(a,b);
  if (0 == rc)
    rc = CompareAppearance(a,b);
  return rc;
}

int ON_Material::CompareNameAndIds( const ON_Material& a, const ON_Material& b )
{
  // do NOT test index or id

  const ON_UUID aid = a.Id();
  const ON_UUID bid = b.Id();
  int rc = ON_UuidCompare( &aid, &bid );
  if (rc) return rc;

  rc = a.Name().CompareOrdinal( static_cast< const wchar_t* >(b.Name()), false );
  if (rc) return rc;

  rc = ON_UuidCompare(&a.m_rdk_material_instance_id, &b.m_rdk_material_instance_id);
  if (rc) return rc;

  const int tcount = a.m_textures.Count();
  rc = tcount - b.m_textures.Count();
  for (int i = 0; i < tcount && 0 == rc; i++)
  {
    rc = ON_UuidCompare(a.m_textures[i].m_texture_id, b.m_textures[i].m_texture_id);
  }

  return rc;  
}


int ON_Material::CompareColorAttributes( const ON_Material& a, const ON_Material& b )
{
  int rc = a.m_ambient.Compare(b.m_ambient);
  if (rc) return rc;

  rc = a.m_diffuse.Compare( b.m_diffuse );
  if (rc) return rc;

  rc = a.m_emission.Compare( b.m_emission );
  if (rc) return rc;

  rc = a.m_specular.Compare( b.m_specular );
  if (rc) return rc;

  rc = a.m_reflection.Compare( b.m_reflection );
  if (rc) return rc;

  rc = a.m_transparent.Compare( b.m_transparent );
  if (rc) return rc;

  rc = CompareDouble(a.m_transparency,b.m_transparency);
  if (rc) return rc;

  rc = ((int)a.m_bDisableLighting) - ((int)b.m_bDisableLighting);

  return rc;  
}


int ON_Material::CompareReflectionAttributes( const ON_Material& a, const ON_Material& b )
{
  int rc = a.m_reflection.Compare( b.m_reflection );
  if (0 != rc) return rc;

  rc = CompareDouble(a.m_index_of_refraction,b.m_index_of_refraction);
  if (0 != rc) return rc;

  rc = CompareDouble(a.m_reflectivity,b.m_reflectivity);
  if (0 != rc) return rc;

  rc = CompareDouble(a.m_shine,b.m_shine);
  if (0 != rc) return rc;

  rc = (a.m_bFresnelReflections?1:0) - (b.m_bFresnelReflections?1:0);
  if (0 != rc) return rc;
  if ( a.m_bFresnelReflections )
  {
    rc = CompareDouble(a.m_fresnel_index_of_refraction,b.m_fresnel_index_of_refraction);
    if (0 != rc) return rc;
  }

  rc = CompareDouble(a.m_reflection_glossiness,b.m_reflection_glossiness);
  if (0 != rc) return rc;

  rc = CompareDouble(a.m_refraction_glossiness,b.m_refraction_glossiness);


  return rc;  
}

int ON_Material::CompareTextureAttributes(const ON_Material& a, const ON_Material& b)
{
  // do NOT test index or id

  const int tcount = a.m_textures.Count();
  int rc = tcount - b.m_textures.Count();
  for (int i = 0; i < tcount && 0 == rc; i++)
  {
    rc = ON_Texture::Compare(a.m_textures[i], b.m_textures[i]);
  }
  if (0 == rc)
    rc = ((int)a.m_bUseDiffuseTextureAlphaForObjectTransparencyTexture) - ((int)b.m_bUseDiffuseTextureAlphaForObjectTransparencyTexture);


  return rc;
}

int ON_Material::CompareTextureAttributesAppearance(const ON_Material& a, const ON_Material& b)
{
  // do NOT test index or id

  const int tcount = a.m_textures.Count();
  int rc = tcount - b.m_textures.Count();
  for (int i = 0; i < tcount && 0 == rc; i++)
  {
    rc = ON_Texture::CompareAppearance(a.m_textures[i], b.m_textures[i]);
  }
  if (0 == rc)
    rc = ((int)a.m_bUseDiffuseTextureAlphaForObjectTransparencyTexture) - ((int)b.m_bUseDiffuseTextureAlphaForObjectTransparencyTexture);


  return rc;
}

int ON_Material::CompareAppearance( const ON_Material& a, const ON_Material& b )
{
  int rc = CompareColorAttributes(a,b);
  if ( 0 == rc )
    rc = CompareReflectionAttributes(a,b);
  if ( 0 == rc )
    rc = CompareTextureAttributesAppearance(a,b);

  if ( 0 == rc )
    rc = ON_UuidCompare( &a.m_plugin_id, &b.m_plugin_id );

  return rc;
}




ON_UUID ON_Material::RdkMaterialInstanceId() const
{
  return m_rdk_material_instance_id;
}

/*
Description:
Set this material's RDK material id.
Parameters:
rdk_material_id - [in]
RDK material id value.
Remarks:
The RDK material id identifies a material definition managed by
the RDK (rendering development kit).  Multiple materials in
a Rhino or opennurbs model can reference the same RDK material.
*/
void ON_Material::SetRdkMaterialInstanceId(
  ON_UUID rdk_material_instance_id
  )
{
  m_rdk_material_instance_id = rdk_material_instance_id;
}

bool ON_Material::RdkMaterialInstanceIdIsNotNil() const
{
  return (!(ON_nil_uuid == m_rdk_material_instance_id));
}

bool ON_Material::RdkMaterialInstanceIdIsNil() const
{
  return (ON_nil_uuid == m_rdk_material_instance_id);
}

// NO ON_OBJECT_IMPLEMENT(ON_RdkMaterialInstanceIdObsoleteUserData, ON_ObsoleteUserData, ...)
// because ON_RdkMaterialInstanceIdObsoleteUserData is derived from ON_ObsoleteUserData.

// CRhRdkUserData class id valud
//  = ON_RdkMaterialInstanceIdObsoleteUserData::ClassId()->Uuid()
//  = AFA82772-1525-43dd-A63C-C84AC5806911
// From CRhRdkUserData ON_OBJECT_IMPLEMENT macro
//   file: http://subversion.mcneel.com/rhino/6/trunk/src4/rhino4/Plug-ins/RDK/RDK/RhRcmUserData.cpp
//   revision: 102101
//
// {AFA82772-1525-43dd-A63C-C84AC5806911}
const ON_UUID ON_RdkMaterialInstanceIdObsoleteUserData::m_archive_class_id_ctor =
{ 0xAFA82772, 0x1525, 0x43dd, { 0xA6, 0x3C, 0xC8, 0x4A, 0xC5, 0x80, 0x69, 0x11 } };

// CRhRdkUserData::m_userdata_uuid value
//  = CRhRdkUserData::Uuid()
//  = CRhRdkUserData::m_Uuid
//  = B63ED079-CF67-416c-800D-22023AE1BE21
// From
//   file: http://subversion.mcneel.com/rhino/6/trunk/src4/rhino4/Plug-ins/RDK/RDK/RhRcmUserData.cpp
//   revision: 102101
//
// {B63ED079-CF67-416c-800D-22023AE1BE21}
const ON_UUID ON_RdkMaterialInstanceIdObsoleteUserData::m_archive_userdata_uuid_ctor =
{ 0xb63ed079, 0xcf67, 0x416c, { 0x80, 0xd, 0x22, 0x2, 0x3a, 0xe1, 0xbe, 0x21 } };

// CRhRdkUserData::m_application_uuid value 
//  = CRhRdkRhinoPlugIn::RhinoPlugInUuid()
//  = CRhRdkRhinoPlugIn::m_uuidRhinoPlugIn
//  = 16592D58-4A2F-401D-BF5E-3B87741C1B1B
// From 
//  file: http://subversion.mcneel.com/rhino/6/trunk/src4/rhino4/Plug-ins/RDK/RDK/RhRcmRhinoPlugIn.cpp
//  revision: 102101
//
// {16592D58-4A2F-401D-BF5E-3B87741C1B1B}
const ON_UUID ON_RdkMaterialInstanceIdObsoleteUserData::m_archive_application_uuid_ctor =
{ 0x16592D58, 0x4A2F, 0x401D, { 0xBF, 0x5E, 0x3B, 0x87, 0x74, 0x1C, 0x1B, 0x1B } };

const unsigned int ON_RdkMaterialInstanceIdObsoleteUserData::m_userdata_copycount_ctor = 1;

const ON_Xform ON_RdkMaterialInstanceIdObsoleteUserData::m_userdata_xform_ctor(ON_Xform::IdentityTransformation);

ON_RdkMaterialInstanceIdObsoleteUserData::ON_RdkMaterialInstanceIdObsoleteUserData()
: m_rdk_material_instance_id(ON_nil_uuid)
{
  ///////////////////////////////////////////////////////////
  // ON_UserData field initialization:

  // The values of m_userdata_uuid and m_application_uuid match those used by CRhRdkUserData.
  m_userdata_uuid = ON_RdkMaterialInstanceIdObsoleteUserData::m_archive_userdata_uuid_ctor;
  m_application_uuid = ON_RdkMaterialInstanceIdObsoleteUserData::m_archive_application_uuid_ctor;

  // Values for the 3dm archive.
  m_userdata_copycount = ON_RdkMaterialInstanceIdObsoleteUserData::m_userdata_copycount_ctor;
  m_userdata_xform = ON_RdkMaterialInstanceIdObsoleteUserData::m_userdata_xform_ctor;

  ///////////////////////////////////////////////////////////
  // ON_ObsoleteUserData field initialization:
  m_archive_class_uuid = ON_RdkMaterialInstanceIdObsoleteUserData::m_archive_class_id_ctor;
}

ON_RdkMaterialInstanceIdObsoleteUserData::~ON_RdkMaterialInstanceIdObsoleteUserData()
{}


ON_RdkMaterialInstanceIdObsoleteUserData::ON_RdkMaterialInstanceIdObsoleteUserData(const ON_RdkMaterialInstanceIdObsoleteUserData& src)
: ON_ObsoleteUserData(src)
, m_rdk_material_instance_id(src.m_rdk_material_instance_id)
{}

ON_RdkMaterialInstanceIdObsoleteUserData& ON_RdkMaterialInstanceIdObsoleteUserData::operator=(const ON_RdkMaterialInstanceIdObsoleteUserData& src)
{
  if (this != &src)
  {
    ON_ObsoleteUserData::operator=(src);
    m_rdk_material_instance_id = src.m_rdk_material_instance_id;
  }
  return *this;
}

bool ON_RdkMaterialInstanceIdObsoleteUserData::GetDescription(ON_wString& description)
{
  description = "RDK material instance id as user data for writing pre V6 file formats.";
  return true;
}

bool ON_RdkMaterialInstanceIdObsoleteUserData::WriteToArchive(
  const class ON_BinaryArchive& archive,
  const class ON_Object* parent_object
  ) const
{
  return (ON_UuidIsNotNil(m_rdk_material_instance_id) && archive.Archive3dmVersion() <= 50);
}

bool ON_RdkMaterialInstanceIdObsoleteUserData::DeleteAfterWrite(
  const ON_BinaryArchive& archive,
  const ON_Object* parent_object
  ) const
{
  // Returning true will cause the ON_BinaryArchive::WriteObject()
  // plumbing to delete this user data.
  return true;
}

bool ON_RdkMaterialInstanceIdObsoleteUserData::DeleteAfterRead(
  const ON_BinaryArchive& archive,
  ON_Object* parent_object
  ) const
{
  // move the RDK material id value from the V5 user data to
  // the V6 ON_Material.m_rdk_material_instance_id field.
  ON_Material* mat = ON_Material::Cast(parent_object);
  if (mat && mat->RdkMaterialInstanceIdIsNil())
    mat->SetRdkMaterialInstanceId(m_rdk_material_instance_id);
  
  // Returning true will cause the ON_BinaryArchive::ReadObject()
  // plumbing to delete this user data.
  return true;
}

bool ON_RdkMaterialInstanceIdObsoleteUserData::IsRdkMaterialInstanceIdUserData(
  ON_UUID class_id,
  ON_UUID userdata_id,
  ON_UUID app_id,
  ON_Object* object
  )
{
  return (
    nullptr != ON_Material::Cast(object)
    && class_id == ON_RdkMaterialInstanceIdObsoleteUserData::m_archive_class_id_ctor
    && userdata_id == ON_RdkMaterialInstanceIdObsoleteUserData::m_archive_userdata_uuid_ctor
    && app_id == ON_RdkMaterialInstanceIdObsoleteUserData::m_archive_application_uuid_ctor
    );
}

static const char* ParsePastWhiteSpace(const char* s)
{
  for (char c = s ? *s++ : 0; 0 != c; c = *s++)
  {
    if (32 == c)
      continue;
    if (c >= 9 && c <= 13)
      continue;
    break;
  }
  return s;
}

static char ToUpper(char c)
{
  if (c >= 'a' && c <= 'z')
    c -= 0x20;
  return c;
}

static const char* ParsePast(const char* token, const char* s)
{
  if (0 == token || token[0] <= 32)
    return 0;
  
  s = ParsePastWhiteSpace(s);
  if (0 == s || s[0] <= 32)
    return 0;
  
  for (/*empty init*/; ToUpper(*s) == ToUpper(*token); s++, token++)
  {
    if (0 == *s)
      return s;
  }
  return 0;
}

bool ON_RdkMaterialInstanceIdObsoleteUserData::Read(
  ON_BinaryArchive& archive
  )
{
  m_rdk_material_instance_id = ON_nil_uuid;

  bool rc = false;
  for (;;)
  {
    int version = 0;
    if (!archive.ReadInt(&version))
      break;
    if (2 != version)
      break;

    int s_length = 0;
    if (!archive.ReadInt(&s_length))
      break;
    if (s_length < 0 || s_length > 1024)
      break;
    if (0 == s_length)
    {
      rc = true;
      break;
    }
    
    ON_String str((char)0, (int)s_length);
    if (str.Length() < s_length)
      break;
    const char* s = str.Array();
    if (0 == s)
      break;

    if (!archive.ReadByte(s_length, (void*)s))
      break;

    // parse the xml the CRhRdkUserData::Write() function
    // put into V5 files and V6 files written before May 16, 2014.

    s = ParsePast("<", s);
    s = ParsePast("xml", s);
    s = ParsePast(">", s);

    s = ParsePast("<", s);
    s = ParsePast("render-content-manager-data", s);
    s = ParsePast(">", s);

    s = ParsePast("<", s);
    s = ParsePast("material", s);
    s = ParsePast("instance-id", s);
    s = ParsePast("=", s);

    s = ParsePast("\"", s);
    s = ParsePastWhiteSpace(s);
    s = ON_ParseUuidString(s, &m_rdk_material_instance_id);
    s = ParsePast("\"", s);

    rc = (0 != s);
    break;
  }

  return rc;
}

bool ON_RdkMaterialInstanceIdObsoleteUserData::Write(
  ON_BinaryArchive& archive
  ) const
{
  // write xml the CRhRdkUserData::Write() function
  // put into V5 files and V6 files written before May 16, 2014.

  char s__rdk_material_instance_id[37];
  ON_String s =
    "<xml>\n"
    "<render-content-manager-data>\n"
    "<material instance-id=\"";
   s += ON_UuidToString(m_rdk_material_instance_id, s__rdk_material_instance_id);
   s += 
    "\" name=\"\" />\n"
    "</render-content-manager-data>\n"
    "</xml>";
   const int s_length = (int)s.Length();
   const char* s_array = s.Array();
   bool rc
     =  archive.WriteInt(2) // "2" was a version number used in V5 files
     && archive.WriteInt(s_length)
     && archive.WriteByte(s_length, s_array);
   return rc;
}


ON_Color ON_Material::Ambient() const
{
  return m_ambient & 0x00FFFFFF;
}

ON_Color ON_Material::Diffuse( ) const
{
  return m_diffuse & 0x00FFFFFF;
}

ON_Color ON_Material::Emission( ) const
{
  return m_emission & 0x00FFFFFF;
}

ON_Color ON_Material::Specular() const
{
  return m_specular & 0x00FFFFFF;
}

void ON_Material::SetAmbient( ON_Color  c )
{
  if (m_ambient != c)
  {
    m_ambient = c;
    IncrementContentVersionNumber();
  }
}

void ON_Material::SetDiffuse(  ON_Color c )
{
  if (m_diffuse != c)
  {
    m_diffuse = c;
    IncrementContentVersionNumber();
  }
}

void ON_Material::SetEmission( ON_Color c )
{
  if (m_emission != c)
  {
    m_emission = c;
    IncrementContentVersionNumber();
  }
}

void ON_Material::SetSpecular( ON_Color c )
{
  if (m_specular != c)
  {
    m_specular = c;
    IncrementContentVersionNumber();
  }
}

bool ON_Material::Shareable() const
{
  return m_bShareable;
}

void ON_Material::SetShareable(
  bool bShareable
  )
{
  if (bShareable != m_bShareable)
  {
    m_bShareable = bShareable?true:false;
    IncrementContentVersionNumber();
  }
}


bool ON_Material::DisableLighting() const
{
  return m_bDisableLighting;
}

void ON_Material::SetDisableLighting(
  bool bDisableLighting
  )
{
  if (bDisableLighting != m_bDisableLighting)
  {
    m_bDisableLighting = bDisableLighting?true:false;
    IncrementContentVersionNumber();
  }
}

//Very simple preview color function that better supports metals and dialectrics.
ON_Color ON_Material::PreviewColor(void) const
{
	if (Transparency() > 0.5)
	{
		return m_transparent;
	}

	if (!FresnelReflections())
	{
		if (Reflectivity() > 0.5)
		{
			return m_reflection;
		}
	}

	return m_diffuse;
}

bool ON_Material::UseDiffuseTextureAlphaForObjectTransparencyTexture() const
{
  return m_bUseDiffuseTextureAlphaForObjectTransparencyTexture;
}

void ON_Material::SetUseDiffuseTextureAlphaForObjectTransparencyTexture(
  bool bUseDiffuseTextureAlphaForObjectTransparencyTexture
  )
{
  if (bUseDiffuseTextureAlphaForObjectTransparencyTexture != m_bUseDiffuseTextureAlphaForObjectTransparencyTexture)
  {
    m_bUseDiffuseTextureAlphaForObjectTransparencyTexture = bUseDiffuseTextureAlphaForObjectTransparencyTexture?true:false;
    IncrementContentVersionNumber();
  }
}
  
bool ON_Material::FresnelReflections() const
{
  return m_bFresnelReflections;
}

void ON_Material::SetFresnelReflections(
  bool bFresnelReflections
  )
{
  if (bFresnelReflections != m_bFresnelReflections)
  {
    m_bFresnelReflections = bFresnelReflections?true:false;
    IncrementContentVersionNumber();
  }
}

////////////////////////////////////////////////////////////////
//   Class ON_Texture
////////////////////////////////////////////////////////////////

ON_OBJECT_IMPLEMENT(ON_Texture,ON_Object,"D6FF106D-329B-4f29-97E2-FD282A618020");

bool ON_Texture::IsValid( ON_TextLog* text_log ) const
{
  if ( ON_Texture::TYPE::no_texture_type == m_type )
  {
    if ( text_log )
    {
      text_log->Print("ON_Texture m_type has invalid value.\n");
    }
    return false;
  }

  // TODO ...

  return true;
}

// overrides virtual ON_Object::Dump
void ON_Texture::Dump( ON_TextLog& ) const
{

}

// overrides virtual ON_Object::SizeOf
unsigned int ON_Texture::SizeOf() const
{
  unsigned int sz = ON_Object::SizeOf();
  sz += sizeof(*this) - sizeof(ON_Object);
  return sz;
}

// overrides virtual ON_Object::Write
bool ON_Texture::Write(
  ON_BinaryArchive& binary_archive
  ) const
{
  const int major_version = 1;
  const int minor_version 
    = binary_archive.Archive3dmVersion() >= 60
    ? 1
    : 0;

  bool rc = binary_archive.BeginWrite3dmChunk(TCODE_ANONYMOUS_CHUNK,major_version,minor_version);
  if (rc)
  {

    for(;;)
    {
      // 1.0 values
      rc = binary_archive.WriteUuid(m_texture_id);
      if (!rc) break;
      rc = binary_archive.WriteInt(m_mapping_channel_id);
      if (!rc) break;
      rc =
        m_image_file_reference.FullPath().IsNotEmpty()
        ? binary_archive.WriteString(m_image_file_reference.FullPath())
        : binary_archive.WriteString(m_image_file_reference.RelativePath());
      if (!rc) break;
      rc = binary_archive.WriteBool(m_bOn);
      if (!rc) break;
      rc = binary_archive.WriteInt(static_cast<unsigned int>(m_type));
      if (!rc) break;
      rc = binary_archive.WriteInt(static_cast<unsigned int>(m_mode));
      if (!rc) break;
      rc = binary_archive.WriteInt(static_cast<unsigned int>(m_minfilter));
      if (!rc) break;
      rc = binary_archive.WriteInt(static_cast<unsigned int>(m_magfilter));
      if (!rc) break;
      rc = binary_archive.WriteInt(static_cast<unsigned int>(m_wrapu));
      if (!rc) break;
      rc = binary_archive.WriteInt(static_cast<unsigned int>(m_wrapv));
      if (!rc) break;
      rc = binary_archive.WriteInt(static_cast<unsigned int>(m_wrapw));
      if (!rc) break;
      rc = binary_archive.WriteXform(m_uvw);
      if (!rc) break;
      rc = binary_archive.WriteColor(m_border_color);
      if (!rc) break;
      rc = binary_archive.WriteColor(m_transparent_color);
      if (!rc) break;
      rc = binary_archive.WriteUuid(m_transparency_texture_id);
      if (!rc) break;
      rc = binary_archive.WriteInterval(m_bump_scale);
      if (!rc) break;
      rc = binary_archive.WriteDouble(m_blend_constant_A);
      if (!rc) break;
      rc = binary_archive.WriteDouble(m_blend_A0);
      if (!rc) break;
      rc = binary_archive.WriteDouble(m_blend_A1);
      if (!rc) break;
      rc = binary_archive.WriteDouble(m_blend_A2);
      if (!rc) break;
      rc = binary_archive.WriteDouble(m_blend_A3);
      if (!rc) break;
      rc = binary_archive.WriteColor(m_blend_constant_RGB);
      if (!rc) break;
      rc = binary_archive.WriteDouble(m_blend_RGB0);
      if (!rc) break;
      rc = binary_archive.WriteDouble(m_blend_RGB1);
      if (!rc) break;
      rc = binary_archive.WriteDouble(m_blend_RGB2);
      if (!rc) break;
      rc = binary_archive.WriteDouble(m_blend_RGB3);
      if (!rc) break;
      rc = binary_archive.WriteInt(m_blend_order);
      if (!rc) break;

      if ( minor_version <= 0 )
        break;
      
      // version 1.1 added m_image_file_reference
      rc = m_image_file_reference.Write(true,binary_archive);
      if (!rc) break;

      break;
    }


    if ( !binary_archive.EndWrite3dmChunk() )
      rc = false;
  }
  return rc;
}

static ON_Texture::MAPPING_CHANNEL Internal_BuiltInMappingChannelFromUnsigned(
  unsigned int built_in_mapping_channel_as_unsigned,
  bool bEnableErrorMessage
  )
{
  switch (built_in_mapping_channel_as_unsigned)
  {
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MAPPING_CHANNEL::tc_channel);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MAPPING_CHANNEL::default_channel);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MAPPING_CHANNEL::screen_based_channel);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MAPPING_CHANNEL::wcs_channel);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MAPPING_CHANNEL::wcs_box_channel);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MAPPING_CHANNEL::environment_map_box_channel);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MAPPING_CHANNEL::environment_map_light_probe_channel);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MAPPING_CHANNEL::environment_map_spherical_channel);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MAPPING_CHANNEL::environment_map_cube_map_channel);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MAPPING_CHANNEL::environment_map_vcross_cube_map_channel);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MAPPING_CHANNEL::environment_map_hcross_cube_map_channel);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MAPPING_CHANNEL::environment_map_hemispherical_channel);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MAPPING_CHANNEL::environment_map_emap_channel);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MAPPING_CHANNEL::srfp_channel);
  //ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MAPPING_CHANNEL::emap_channel);
  }

  if (bEnableErrorMessage)
  {
    ON_ERROR("Invalid built_in_mapping_channel_as_unsigned value.");
  }
  return ON_Texture::MAPPING_CHANNEL::tc_channel;
}

ON_Texture::MAPPING_CHANNEL ON_Texture::BuiltInMappingChannelFromUnsigned(
  unsigned int built_in_mapping_channel_as_unsigned
  )
{
  return Internal_BuiltInMappingChannelFromUnsigned(
    built_in_mapping_channel_as_unsigned,
    true
    );
}


const ON_SHA1_Hash ON_Texture::ContentHash() const
{
  ON_SHA1 sha1;
  sha1.AccumulateSubHash(m_image_file_reference.FullPathHash());
  sha1.AccumulateBool(m_bOn);
  sha1.AccumulateUnsigned32(static_cast<unsigned int>(m_type));
  sha1.AccumulateUnsigned32(static_cast<unsigned int>(m_mode));
  sha1.AccumulateUnsigned32(static_cast<unsigned int>(m_minfilter));
  sha1.AccumulateUnsigned32(static_cast<unsigned int>(m_magfilter));
  sha1.AccumulateUnsigned32(static_cast<unsigned int>(m_wrapu));
  sha1.AccumulateUnsigned32(static_cast<unsigned int>(m_wrapv));
  sha1.AccumulateUnsigned32(static_cast<unsigned int>(m_wrapw));
  sha1.AccumulateTransformation(m_uvw);
  sha1.AccumulateUnsigned32(m_border_color);
  sha1.AccumulateUnsigned32(m_transparent_color);
  sha1.AccumulateId(m_transparency_texture_id);
  sha1.AccumulateDouble(m_bump_scale.m_t[0]);
  sha1.AccumulateDouble(m_bump_scale.m_t[1]);
  sha1.AccumulateDouble(m_blend_constant_A);
  sha1.AccumulateDouble(m_blend_A0);
  sha1.AccumulateDouble(m_blend_A1);
  sha1.AccumulateDouble(m_blend_A2);
  sha1.AccumulateDouble(m_blend_A3);
  sha1.AccumulateDouble(m_blend_constant_RGB);
  sha1.AccumulateDouble(m_blend_RGB0);
  sha1.AccumulateDouble(m_blend_RGB1);
  sha1.AccumulateDouble(m_blend_RGB2);
  sha1.AccumulateDouble(m_blend_RGB3);
  sha1.AccumulateInteger32(m_blend_order);
  return sha1.Hash();
}


bool ON_Texture::IsBuiltInMappingChannel(
  unsigned int mapping_channel_id
  )
{
  ON_Texture::MAPPING_CHANNEL mc = Internal_BuiltInMappingChannelFromUnsigned(mapping_channel_id,false);
  return (static_cast<unsigned int>(mc) == mapping_channel_id);
}

void ON_Texture::SetBuiltInMappingChannel(
  ON_Texture::MAPPING_CHANNEL built_in_mapping_channel_as_unsigned
  )
{
  SetMappingChannel( static_cast<unsigned int>(built_in_mapping_channel_as_unsigned) );
}

void ON_Texture::SetMappingChannel(
  unsigned int mapping_channel_id
  )
{
  m_mapping_channel_id = mapping_channel_id;
}

ON_Texture::TYPE ON_Texture::TypeFromUnsigned( unsigned int type_as_unsigned )
{
  switch(type_as_unsigned)
  {
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::TYPE::no_texture_type );
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::TYPE::bitmap_texture);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::TYPE::bump_texture);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::TYPE::emap_texture);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::TYPE::transparency_texture);
  }

  ON_ERROR("Invalid type_as_unsigned value.");
  return ON_Texture::TYPE::no_texture_type;
}

ON_Texture::MODE ON_Texture::ModeFromUnsigned( unsigned int mode_as_unsigned )
{
  switch(mode_as_unsigned)
  {
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MODE::no_texture_mode);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MODE::modulate_texture);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MODE::decal_texture);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::MODE::blend_texture);
  }

  ON_ERROR("Invalid mode_as_unsigned value.");
  return ON_Texture::MODE::no_texture_mode;
}

ON_Texture::FILTER ON_Texture::FilterFromUnsigned( unsigned int filter_as_unsigned )
{
  switch(filter_as_unsigned)
  {
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::FILTER::nearest_filter);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::FILTER::linear_filter);
  }

  ON_ERROR("Invalid filter_as_unsigned value.");
  return ON_Texture::FILTER::linear_filter;
}

ON_Texture::WRAP ON_Texture::WrapFromUnsigned( unsigned int wrap_as_unsigned )
{

  switch(wrap_as_unsigned)
  {
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::WRAP::repeat_wrap);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_Texture::WRAP::clamp_wrap);
  }

  ON_ERROR("Invalid wrap_as_unsigned value.");
  return ON_Texture::WRAP::repeat_wrap;
}

bool ON_Texture::Read(
  ON_BinaryArchive& binary_archive
  )
{
  *this = ON_Texture::Default;

  int major_version = 0;
  int minor_version = 0;
  bool rc = binary_archive.BeginRead3dmChunk(TCODE_ANONYMOUS_CHUNK,&major_version,&minor_version);
  if (rc)
  {

    if ( 1 != major_version )
    {
      rc = false;
    }
    else
    {
      unsigned int i;
      for(;;)
      {
        // 1.0 values
        rc = binary_archive.ReadUuid( m_texture_id );
        if (!rc) break;

        rc = binary_archive.ReadInt( &m_mapping_channel_id );
        if (!rc) break;

        ON_wString filename;
        rc = binary_archive.ReadString(filename);
        if (!rc) break;
        if (ON_FileSystemPath::IsRelativePath(filename))
          m_image_file_reference.SetRelativePath(filename);
        else
          m_image_file_reference.SetFullPath(filename,false);

        rc = binary_archive.ReadBool(&m_bOn);
        if (!rc) break;

        rc = binary_archive.ReadInt(&i);
        if (!rc) break;
        m_type = ON_Texture::TypeFromUnsigned(i);

        rc = binary_archive.ReadInt(&i);
        if (!rc) break;
        m_mode = ON_Texture::ModeFromUnsigned(i);

        rc = binary_archive.ReadInt(&i);
        if (!rc) break;
        m_minfilter = ON_Texture::FilterFromUnsigned(i);

        rc = binary_archive.ReadInt(&i);
        if (!rc) break;
        m_magfilter = ON_Texture::FilterFromUnsigned(i);

        rc = binary_archive.ReadInt(&i);
        if (!rc) break;
        m_wrapu = ON_Texture::WrapFromUnsigned(i);

        rc = binary_archive.ReadInt(&i);
        if (!rc) break;
        m_wrapv = ON_Texture::WrapFromUnsigned(i);

        rc = binary_archive.ReadInt(&i);
        if (!rc) break;
        m_wrapw = ON_Texture::WrapFromUnsigned(i);

        rc = binary_archive.ReadXform(m_uvw);
        if (!rc) break;

        rc = binary_archive.ReadColor(m_border_color);
        if (!rc) break;

        rc = binary_archive.ReadColor(m_transparent_color);
        if (!rc) break;

        rc = binary_archive.ReadUuid(m_transparency_texture_id);
        if (!rc) break;

        rc = binary_archive.ReadInterval(m_bump_scale);
        if (!rc) break;

        rc = binary_archive.ReadDouble(&m_blend_constant_A);
        if (!rc) break;
        rc = binary_archive.ReadDouble(&m_blend_A0);
        if (!rc) break;
        rc = binary_archive.ReadDouble(&m_blend_A1);
        if (!rc) break;
        rc = binary_archive.ReadDouble(&m_blend_A2);
        if (!rc) break;
        rc = binary_archive.ReadDouble(&m_blend_A3);
        if (!rc) break;
        rc = binary_archive.ReadColor(m_blend_constant_RGB);
        if (!rc) break;
        rc = binary_archive.ReadDouble(&m_blend_RGB0);
        if (!rc) break;
        rc = binary_archive.ReadDouble(&m_blend_RGB1);
        if (!rc) break;
        rc = binary_archive.ReadDouble(&m_blend_RGB2);
        if (!rc) break;
        rc = binary_archive.ReadDouble(&m_blend_RGB3);
        if (!rc) break;

        rc = binary_archive.ReadInt(&m_blend_order);
        if (!rc) break;

        if ( minor_version <= 0 )
          break;

        rc = m_image_file_reference.Read(binary_archive);
        if (!rc) break;

        break;
      }
    }

    if ( !binary_archive.EndRead3dmChunk() )
      rc = false;
  }
  return rc;
}


ON_OBJECT_IMPLEMENT(ON_TextureMapping,ON_ModelComponent,"32EC997A-C3BF-4ae5-AB19-FD572B8AD554");


const ON_TextureMapping* ON_TextureMapping::FromModelComponentRef(
  const class ON_ModelComponentReference& model_component_reference,
  const ON_TextureMapping* none_return_value
  )
{
  const ON_TextureMapping* p = ON_TextureMapping::Cast(model_component_reference.ModelComponent());
  return (nullptr != p) ? p : none_return_value;
}

ON_TextureMapping::TYPE ON_TextureMapping::TypeFromUnsigned(
  unsigned int type_as_unsigned
  )
{
  switch (type_as_unsigned)
  {
  ON_ENUM_FROM_UNSIGNED_CASE(ON_TextureMapping::TYPE::no_mapping);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_TextureMapping::TYPE::srfp_mapping);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_TextureMapping::TYPE::plane_mapping);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_TextureMapping::TYPE::cylinder_mapping);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_TextureMapping::TYPE::sphere_mapping);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_TextureMapping::TYPE::box_mapping);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_TextureMapping::TYPE::mesh_mapping_primitive);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_TextureMapping::TYPE::srf_mapping_primitive);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_TextureMapping::TYPE::brep_mapping_primitive);
  }

  ON_ERROR("Invalid type_as_unsigned value.");
  return ON_TextureMapping::TYPE::no_mapping;
}

const ON_wString ON_TextureMapping::TypeToString(ON_TextureMapping::TYPE texture_mapping_type)
{
  switch (texture_mapping_type)
  {
  ON_ENUM_TO_WIDE_STRING_CASE(ON_TextureMapping::TYPE::no_mapping);
  ON_ENUM_TO_WIDE_STRING_CASE(ON_TextureMapping::TYPE::srfp_mapping);
  ON_ENUM_TO_WIDE_STRING_CASE(ON_TextureMapping::TYPE::plane_mapping);
  ON_ENUM_TO_WIDE_STRING_CASE(ON_TextureMapping::TYPE::cylinder_mapping);
  ON_ENUM_TO_WIDE_STRING_CASE(ON_TextureMapping::TYPE::sphere_mapping);
  ON_ENUM_TO_WIDE_STRING_CASE(ON_TextureMapping::TYPE::box_mapping);
  ON_ENUM_TO_WIDE_STRING_CASE(ON_TextureMapping::TYPE::mesh_mapping_primitive);
  ON_ENUM_TO_WIDE_STRING_CASE(ON_TextureMapping::TYPE::srf_mapping_primitive);
  ON_ENUM_TO_WIDE_STRING_CASE(ON_TextureMapping::TYPE::brep_mapping_primitive);
  }

  ON_ERROR("Invalid texture_mapping_type value.");
  return ON_wString::EmptyString;
}


ON_TextureMapping::PROJECTION ON_TextureMapping::ProjectionFromUnsigned(
  unsigned int projection_as_unsigned
  )
{
  switch (projection_as_unsigned)
  {
  ON_ENUM_FROM_UNSIGNED_CASE(ON_TextureMapping::PROJECTION::no_projection);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_TextureMapping::PROJECTION::clspt_projection);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_TextureMapping::PROJECTION::ray_projection);
  }

  ON_ERROR("Invalid projection_as_unsigned value.");
  return ON_TextureMapping::PROJECTION::no_projection;
}

const ON_wString ON_TextureMapping::ProjectionToString(ON_TextureMapping::PROJECTION texture_mapping_projection)
{
  switch (texture_mapping_projection)
  {
  ON_ENUM_TO_WIDE_STRING_CASE(ON_TextureMapping::PROJECTION::no_projection);
  ON_ENUM_TO_WIDE_STRING_CASE(ON_TextureMapping::PROJECTION::clspt_projection);
  ON_ENUM_TO_WIDE_STRING_CASE(ON_TextureMapping::PROJECTION::ray_projection);
  }

  ON_ERROR("Invalid texture_mapping_projection value.");
  return ON_wString::EmptyString;
}

ON_TextureMapping::TEXTURE_SPACE ON_TextureMapping::TextureSpaceFromUnsigned(
  unsigned int texture_space_as_unsigned
  )
{
  switch (texture_space_as_unsigned)
  {
  ON_ENUM_FROM_UNSIGNED_CASE(ON_TextureMapping::TEXTURE_SPACE::single);
  ON_ENUM_FROM_UNSIGNED_CASE(ON_TextureMapping::TEXTURE_SPACE::divided);
  }
  
  ON_ERROR("Invalid texture_space_as_unsigned value.");
  return ON_TextureMapping::TEXTURE_SPACE::single;
}

const ON_wString ON_TextureMapping::SpaceToString(ON_TextureMapping::TEXTURE_SPACE texture_mapping_space)
{
  switch (texture_mapping_space)
  {
  ON_ENUM_TO_WIDE_STRING_CASE(ON_TextureMapping::TEXTURE_SPACE::single);
  ON_ENUM_TO_WIDE_STRING_CASE(ON_TextureMapping::TEXTURE_SPACE::divided);
  }
  
  ON_ERROR("Invalid texture_mapping_space value.");
  return ON_wString::EmptyString;
}

ON_TextureMapping::ON_TextureMapping() ON_NOEXCEPT
  : ON_ModelComponent(ON_ModelComponent::Type::TextureMapping)
{}

ON_TextureMapping::~ON_TextureMapping()
{
  Internal_Destroy();
}

ON_TextureMapping::ON_TextureMapping( const ON_TextureMapping& src)
  : ON_ModelComponent(ON_ModelComponent::Type::TextureMapping,src)
{
  Internal_CopyFrom(src);
}

ON_TextureMapping& ON_TextureMapping::operator=(const ON_TextureMapping& src)
{
  if ( this != &src )
  {
    Internal_Destroy();
    ON_ModelComponent::operator=(src);
    Internal_CopyFrom(src);
  }
  return *this;
}

void ON_TextureMapping::Internal_Destroy()
{
  PurgeUserData();

  m_mapping_primitive.reset();
}

void ON_TextureMapping::Internal_CopyFrom(const ON_TextureMapping& src)
{
  m_type				= src.m_type;
  m_projection			= src.m_projection;
  m_bCapped				= src.m_bCapped;
  m_texture_space		= src.m_texture_space;
  m_Pxyz				= src.m_Pxyz;
  m_Nxyz				= src.m_Nxyz;
  m_uvw					= src.m_uvw;
  m_mapping_primitive	= src.m_mapping_primitive;
}

bool ON_TextureMapping::IsValid( ON_TextLog* text_log ) const
{
  if ( m_type != ON_TextureMapping::TypeFromUnsigned( static_cast<unsigned int>(m_type) ) )
  {
    if ( text_log )
    {
      text_log->Print("ON_TextureMapping m_type = %d is not a valid value.\n",m_type);
    }
    return false;
  }

  if ( m_projection != ON_TextureMapping::ProjectionFromUnsigned( static_cast<unsigned int>(m_projection) ) )
  {
    if ( text_log )
    {
      text_log->Print("ON_TextureMapping m_projection = %d is not a valid value.\n",m_projection);
    }
    return false;
  }

  if (m_texture_space != ON_TextureMapping::TextureSpaceFromUnsigned( static_cast<unsigned int>(m_texture_space)))
  {
	  if (text_log)
	  {
		  text_log->Print("ON_TextureMapping m_texture_space = %d is not a valid value.\n",m_texture_space);
	  }
	  return false;
  }

  return true;
}

void ON_TextureMapping::Dump( ON_TextLog& text_log ) const
{
  ON_ModelComponent::Dump(text_log);

  text_log.PushIndent();

  const ON_wString type(ON_TextureMapping::TypeToString(m_type));
  text_log.Print("m_type = %ls\n",static_cast<const wchar_t*>(type));

  const ON_wString projection(ON_TextureMapping::ProjectionToString(m_projection));
  text_log.Print("m_projection = %ls\n",static_cast<const wchar_t*>(projection));

  const ON_wString texture_space(ON_TextureMapping::SpaceToString(m_texture_space));
  text_log.Print("m_texture_space = %ls\n",static_cast<const wchar_t*>(texture_space));

  text_log.Print("m_Pxyz =\n");
  text_log.PushIndent();
  text_log.Print(m_Pxyz);
  text_log.PopIndent();

  text_log.Print("m_Nxyz =\n");
  text_log.PushIndent();
  text_log.Print(m_Nxyz);
  text_log.PopIndent();

  text_log.Print("m_uvw =\n");
  text_log.PushIndent();
  text_log.Print(m_uvw);
  text_log.PopIndent();

  text_log.PopIndent();
}

unsigned int ON_TextureMapping::SizeOf() const
{
  unsigned int sz = ON_Object::SizeOf();
  sz = sizeof(*this) - sizeof(ON_Object);
  return sz;
}


ON_Xform ON_Texture::GetPictureShrinkSurfaceTransformation(
  const class ON_Brep* original,
  const class ON_Brep* shrunk,
  const ON_Xform* error_return
)
{
  const class ON_Surface* original_srf 
    = (nullptr != original && 1 == original->m_F.Count())
    ? original->m_F[0].SurfaceOf()
    : nullptr;
  const class ON_Surface* shrunk_srf 
    = (nullptr != shrunk && 1 == shrunk->m_F.Count())
    ? shrunk->m_F[0].SurfaceOf()
    : nullptr;
  return ON_Texture::GetPictureShrinkSurfaceTransformation(
    original_srf,
    shrunk_srf,
    error_return
  );
}

ON_Xform ON_Texture::GetPictureShrinkSurfaceTransformation(
  const class ON_Surface* original,
  const class ON_Surface* shrunk,
  const ON_Xform* error_return
)
{
  ON_Interval original_udomain;
  ON_Interval original_vdomain; 
  ON_Interval shrunk_udomain;
  ON_Interval shrunk_vdomain;
  if (nullptr != original)
  {
    original_udomain = original->Domain(0);
    original_vdomain = original->Domain(1);
  }
  if (nullptr != shrunk)
  {
    shrunk_udomain = shrunk->Domain(0);
    shrunk_vdomain = shrunk->Domain(1);
  }
  return ON_Texture::GetPictureShrinkSurfaceTransformation(
    original_udomain, original_vdomain,
    shrunk_udomain, shrunk_vdomain,
    error_return
  );
}

ON_Xform ON_Texture::GetPictureShrinkSurfaceTransformation(
  const class ON_Interval& original_udomain,
  const class ON_Interval& original_vdomain,
  const class ON_Interval& shrunk_udomain,
  const class ON_Interval& shrunk_vdomain,
  const ON_Xform* error_return
)
{
  if (nullptr == error_return)
    error_return = &ON_Xform::Nan;

  if (false == original_udomain.IsIncreasing())
    return *error_return;
  if (false == original_vdomain.IsIncreasing())
    return *error_return;

  if (false == shrunk_udomain.IsIncreasing())
    return *error_return;
  if (false == shrunk_vdomain.IsIncreasing())
    return *error_return;

  if (false == original_udomain.Includes(shrunk_udomain, false))
    return *error_return;
  if (false == original_vdomain.Includes(shrunk_vdomain, false))
    return *error_return;
  if (false == original_udomain.Includes(shrunk_udomain, true) && false == original_vdomain.Includes(shrunk_vdomain, true))
    return *error_return;

  const ON_3dPoint p0(original_udomain.NormalizedParameterAt(shrunk_udomain[0]), original_vdomain.NormalizedParameterAt(shrunk_vdomain[0]),0.0);
  const ON_3dPoint p1(original_udomain.NormalizedParameterAt(shrunk_udomain[1]), original_vdomain.NormalizedParameterAt(shrunk_vdomain[1]),0.0);
  if (!(0.0 <= p0.x && p0.x < p1.x && p1.x <= 1.0))
    return *error_return;
  if (!(0.0 <= p0.y && p0.y < p1.y && p1.y <= 1.0))
    return *error_return;

  const double sx = shrunk_udomain.Length() / original_udomain.Length();
  if (!(sx > 0.0 && sx <= 1.0))
    return *error_return;
  const double sy = shrunk_vdomain.Length() / original_vdomain.Length();
  if (!(sx > 0.0 && sx <= 1.0))
    return *error_return;

  // The new brep has a smaller surface.
  // Adust the texture transform to use the proper subset of the old picture image texture.
  ON_Xform x
    = ON_Xform::TranslationTransformation(p0 - ON_3dPoint::Origin)
    * ON_Xform::ScaleTransformation(ON_3dPoint::Origin, sx, sy, 1.0);

  return x;
}

bool ON_TextureMapping::ReverseTextureCoordinate( int dir )
{
  bool rc = false;
  if ( 0 <= dir && dir <= 3 )
  {
    ON_Xform x(ON_Xform::IdentityTransformation);
    x.m_xform[dir][dir] = -1.0;
    x.m_xform[dir][3] = 1.0;
    m_uvw = x*m_uvw;
    rc = true;
  }
  return rc;
}

bool ON_TextureMapping::SwapTextureCoordinate( int i, int j )
{
  bool rc = false;
  if (i!=j && 0 <= i && i <= 3 && 0 <= j && j <= 3)
  {
    ON_Xform x(ON_Xform::IdentityTransformation);
    x.m_xform[i][i] = x.m_xform[j][j] = 0.0;
    x.m_xform[i][j] = x.m_xform[j][i] = 1.0;
    m_uvw = x*m_uvw;
    rc = true;
  }
  return rc;
}

bool ON_TextureMapping::TileTextureCoordinate( int dir, double count, double offset )
{
  bool rc = false;
  if ( 0 <= dir && dir <= 3 && 0.0 != count && ON_IsValid(count) && ON_IsValid(offset) )
  {
    ON_Xform x(ON_Xform::IdentityTransformation);
    x.m_xform[dir][dir] = count;
    x.m_xform[dir][3] = offset;
    m_uvw = x*m_uvw;
    rc = true;
  }
  return rc;
}


bool ON_Texture::ReverseTextureCoordinate( int dir )
{
  bool rc = false;
  if ( 0 <= dir && dir <= 3 )
  {
    ON_Xform x(ON_Xform::IdentityTransformation);
    x.m_xform[dir][dir] = -1.0;
    x.m_xform[dir][3] = 1.0;
    m_uvw = x*m_uvw;
    rc = true;
  }
  return rc;
}

bool ON_Texture::SwapTextureCoordinate( int i, int j )
{
  bool rc = false;
  if (i!=j && 0 <= i && i <= 3 && 0 <= j && j <= 3)
  {
    ON_Xform x(ON_Xform::IdentityTransformation);
    x.m_xform[i][i] = x.m_xform[j][j] = 0.0;
    x.m_xform[i][j] = x.m_xform[j][i] = 1.0;
    m_uvw = x*m_uvw;
    rc = true;
  }
  return rc;
}

bool ON_Texture::TileTextureCoordinate( int dir, double count, double offset )
{
  bool rc = false;
  if ( 0 <= dir && dir <= 3 && 0.0 != count && ON_IsValid(count) && ON_IsValid(offset) )
  {
    ON_Xform x(ON_Xform::IdentityTransformation);
    x.m_xform[dir][dir] = count;
    x.m_xform[dir][3] = offset;
    m_uvw = x*m_uvw;
    rc = true;
  }
  return rc;
}

bool ON_Texture::IsTiled( int dir, double* count, double* offset ) const
{
  if ( count )
    *count = 1.0;
  if ( offset )
    *offset = 0.0;

  if ( 0 <= dir && dir <= 3 )
  {
    int row0=-1, row, col;
    for ( row = 0; row < 3; row++ )
    {
      for ( col = 0; col < 3; col++ )
      {
        if ( col != dir && 0.0 != m_uvw.m_xform[row][col] )
          break;
      }
      if ( 3 == col )
      {
        if ( -1 == row0 )
        {
          row0 = row;
        }
        else
          return false;
      }
    }
    if ( row0 >= 0 )
    {
      if (count)
        *count = m_uvw.m_xform[row0][dir];
      if ( offset )
        *offset = m_uvw.m_xform[row0][3];
      return true;
    }
  }

  return false;
}

static const double on__overflow_tol = 1.0e100;

static
int BestHitHelper(double t0, double t1)
{
  return ((t0 < 0.0 && t1 > t0) || (0.0 <= t1 && t1 < t0)) ? 1 : 0;
}

static
int IntersectBoxRayHelper(const ON_3dPoint& rst, const ON_3dVector& n, int dir, double* s)
{
  /*
  returns:
    0 = ray parallel to sides
    1 = ray hit left side (x=-1)
    2 = ray hit right side (x=+1)
    3 = ray hit back side (y=-1)
    4 = ray hit front side (y=+1)
    5 = ray hit bottom side (z=-1)
    6 = ray hit top side (z=+1)
  */
  double nx = (&n.x)[dir];
  ON_3dPoint Q;
  double t,t0,t1;

  // protect against overflow
  t = fabs(nx)*on__overflow_tol;
  t0 = (-1.0 - (&rst.x)[dir]);
  t1 = ( 1.0 - (&rst.x)[dir]);
  if ( fabs(t0) >= t || fabs(t1) >= t )
  {
    *s = ON_UNSET_VALUE;
    return 0;
  }

  t0 /= nx;
  Q = rst + t0*n;
  if ( dir )
  {
    t = Q.x;
    Q.x = Q[dir];
    Q[dir] = t;
  }
  if ( fabs(Q.x+1.0) > ON_SQRT_EPSILON
        || Q.y < -(1.0+ON_SQRT_EPSILON) || Q.y > (1.0+ON_SQRT_EPSILON)
        || Q.z < -(1.0+ON_SQRT_EPSILON) || Q.z > (1.0+ON_SQRT_EPSILON)
        )
  {
    // The ray's intersection with the plane missed the 
    // (-1,+1)x(-1,+1) square that is the side of the box.
    t0 = ON_UNSET_VALUE;
  }

  t1 /= nx;
  Q = rst + t1*n;
  if ( dir )
  {
    t = Q.x;
    Q.x = Q[dir];
    Q[dir] = t;
  }
  if ( fabs(Q.x-1.0) > ON_SQRT_EPSILON
        || Q.y < -(1.0+ON_SQRT_EPSILON) || Q.y > (1.0+ON_SQRT_EPSILON)
        || Q.z < -(1.0+ON_SQRT_EPSILON) || Q.z > (1.0+ON_SQRT_EPSILON)
        )
  {
    // The ray's intersection with the plane missed the 
    // (-1,+1)x(-1,+1) square that is the side of the box.
    t1 = ON_UNSET_VALUE;
    if ( ON_UNSET_VALUE == t0 )
    {
      *s = ON_UNSET_VALUE;
      return 0;
    }
  }

  int rc;
  if ( ON_UNSET_VALUE == t0 || 1 == BestHitHelper(t0,t1) )
  {
    rc = 2 + 2*dir;
    *s = t1;
  }
  else
  {
    rc = 1 + 2*dir;
    *s = t0;
  }
  return rc;
}


int ON_TextureMapping::EvaluatePlaneMapping( 
  const ON_3dPoint& P,
  const ON_3dVector& N,
  ON_3dPoint* T
  ) const
{
  // The matrix m_Pxyz transforms the world  coordinate
  // "mapping rectangle" into the rectangle
  //   -1 <= r <= 1, -1 <= s <= 1, and  (-1 <= t <= 1)

  ON_3dPoint rst(m_Pxyz*P);

  if ( ON_TextureMapping::PROJECTION::ray_projection == m_projection )
  {
    ON_3dVector n(m_Nxyz*N);
    if ( fabs(rst.z) < fabs(n.z)*on__overflow_tol )
    {
      double t = -rst.z/n.z;
      rst.x = rst.x + t*n.x;
      rst.y = rst.y + t*n.y;
    }
  }

  // convert -1 <= r <= 1, -1 <= s <= 1
  // to normalized texture coordinate
	rst.x = 0.5*rst.x + 0.5;
	rst.y = 0.5*rst.y + 0.5;

  // Apply texture coordinate transformation 
  *T = m_uvw*rst;

  //See docs - if m_bCapped is false, then planar is truely flat.
  if (!m_bCapped)
	  T->z = 0.0;

  return 1;
}

int ON_TextureMapping::EvaluateSphereMapping( 
											  const ON_3dPoint& P,
											  const ON_3dVector& N,
											  ON_3dPoint* T
											  ) const
{
  // The matrix m_Pxyz transforms the world coordinate
  // "mapping sphere" into the sphere centered at
  // rst = (0,0,0) with radius 1.0.

  ON_3dPoint rst(m_Pxyz*P);
	const double r = ((const ON_3dVector*)(&rst.x))->Length();
	double t0, t1;
	
	if ( ON_TextureMapping::PROJECTION::ray_projection == m_projection )
	{
		ON_3dVector n(m_Nxyz*N);
		// Shoot a ray from P in the direction N and see if it 
		// hits the sphere.
		int rc = ON_SolveQuadraticEquation( (n.x*n.x+n.y*n.y+n.z*n.z), 
			2.0*(rst.x*n.x+rst.y*n.y+rst.z*n.z), 
			(rst.x*rst.x+rst.y*rst.y+rst.z*rst.z) - 1.0, 
			&t0, &t1 );
		if (rc >= 0 )
		{
			if ( 2 != rc && 1 == BestHitHelper(t0,t1) )
			{
				t0 = t1;
			}
			rst = rst + t0*n;
		}
	}
	
	// convert sphere 3d location to longitude, latitude, radius
	double longitude = (0.0 != rst.y || 0.0 != rst.x) 
		? atan2(rst.y,rst.x) 
		: 0.0;
	double latitude = (0.0 != rst.z) 
		? atan2(rst.z,((const ON_2dVector*)(&rst.x))->Length()) 
		: 0.0;
	if ( latitude > ON_PI )
		latitude -= 2.0*ON_PI;
	
  // convert longitude to normalized texture coordinate
	rst.x = 0.5*longitude/ON_PI;
	if ( rst.x < -ON_EPSILON )
		rst.x += 1.0;
	else if (rst.x < 0.0)
		rst.x = 0.0;
	else if (rst.x > 1.0)
		rst.x = 1.0;

  // convert longitude to normalized texture coordinate
	rst.y = latitude/ON_PI + 0.5;
  if ( rst.y <= 0.0 )
    rst.y = 0.0;
	else if ( rst.y > 1.0 )
		  rst.y = 1.0;
	
  // radius is already normalized
	rst.z = r;
	
  // apply texture coordinate transformation
	*T = m_uvw*rst;

  return 1;
}

int ON_TextureMapping::EvaluateCylinderMapping( 
												const ON_3dPoint& P,
												const ON_3dVector& N,
												ON_3dPoint* T
												) const
{
  // The matrix m_Pxyz transforms the world coordinate
  // "mapping cylinder" into the cylinder centered at
  // rst = (0,0,0) with radius 1.0.  The axis runs
  // from rst = (0,0,-1) to rst = (0,0,+1).

	ON_3dPoint rst(m_Pxyz*P);

	ON_3dPoint Q;
	const double r = ((const ON_2dVector*)(&rst.x))->Length();
	double t, t0, t1;
	int side0, side1;
	PROJECTION mapping_proj = m_projection;
	
	side0 = 0;
	if ( ON_TextureMapping::PROJECTION::ray_projection == mapping_proj )
	{
		ON_3dVector n(m_Nxyz*N);
		t = 0.0;
		
		if ( m_bCapped )
		{
			// shoot at caps
			//  The < t check prevents overflow when the 
			//  ray is nearly parallel to the cap.
			t = fabs(n.z)*on__overflow_tol;
			if ( fabs(1.0+rst.z) < t && fabs(1.0-rst.z) < t )
			{
				side0 = 2;
				side1 = 3;

				t0 = (-1.0 - rst.z)/n.z;
				Q = rst + t0*n;
				if ( fabs(1.0+Q.z) > ON_SQRT_EPSILON
					|| (Q.x*Q.x + Q.y*Q.y) > 1.0 + 2.0*ON_SQRT_EPSILON + ON_EPSILON )
				{
          // The ray's intersection with the bottom plane missed the 
          // radius 1 disk that is the bottom of the cylinder.
					side0 = 0;
				}

				t1 = ( 1.0 - rst.z)/n.z;
				Q = rst + t1*n;
				if ( fabs(1.0-Q.z) > ON_SQRT_EPSILON
					|| (Q.x*Q.x + Q.y*Q.y) > 1.0 + 2.0*ON_SQRT_EPSILON + ON_EPSILON )
				{
          // The ray's intersection with the top plane missed the 
          // radius 1 disk that is the top of the cylinder.
					side1 = 0;
				}
				if ( 0 == side0 || 1 == BestHitHelper(t0,t1) )
				{
					side0 = side1;
					t = t1;
				}
				else
				{
					t = t0;
				}
			}
		}
		
		// shoot ray at the cylinder wall
		int rc = ON_SolveQuadraticEquation( (n.x*n.x+n.y*n.y), 
			2.0*(rst.x*n.x+rst.y*n.y), 
			(rst.x*rst.x+rst.y*rst.y) - 1.0, 
			&t0, &t1 );
		if (rc >= 0 )
		{
			if ( 2 != rc  && 1 == BestHitHelper(t0,t1) )
			{
				t0 = t1;
			}
			if ( 0 == side0 )
			{
				// Either the caps are missing or the ray missed the caps.
        // The best hit is the cylinder wall.
				side0 = 1;
				rst = rst + t0*n;
			}
			else if ( 1 != BestHitHelper(t0,t) )
			{
				// The cylinder is capped and the ray hit the cap, 
        // hit the infinite cylinder wall, and the wall 
        // hit is "first".  If the ray hits the finite 
        // cylinder wall, the I will use the wall hit.
				t1 = rst.z + t0*n.z;
				if ( t1 >= -(1.0+ON_SQRT_EPSILON) && t1 <= 1.0+ON_SQRT_EPSILON )
				{
					// use the hit on the cylinder wall
					side0 = 1;
					rst.x = rst.x + t0*n.x;
					rst.y = rst.y + t0*n.y;
          rst.x = t1;
				}
			}
		}
		
		if ( side0 > 1 )
		{
			// best hit is on a cap
			rst = rst + t*n;
		}
	}
	
	if ( m_bCapped && 0 == side0 )
	{
    if ( fabs(rst.z) > 1.0+ON_SQRT_EPSILON )
    {
      if ( fabs(rst.z) > r )
      {
        side0 = (rst.z < 0.0) ? 2 : 3;
      }
    }
    else if ( r <= 1.001 )
    {
      // The point is inside the capped cylinder.
      // Use normal to dermine which surface to use
      // for closest point test.
		  ON_3dVector n(m_Nxyz*N);
      if (  ( fabs(n.z) > fabs(n.x) && fabs(n.z) > fabs(n.y) ) )
      {
        side0 = (n.z < 0.0) ? 2 : 3;
      }
    }
	}
	
	if ( 2 == side0 || 3 == side0 )
	{
    // The cylinder is capped and P maps to 
    // the top (1 == side0) or bottom (2 == side0)

    if ( 2 == side0 )
    {
      // This is the same convention as box mapping.
      // Put another way, if you change the mapping 
      // between box and cylinder, you get the same
      // picture on the top and bottom.
      rst.x = -rst.x; 
    }

		if ( ON_TextureMapping::TEXTURE_SPACE::divided == m_texture_space )
		{
		  if ( r >= 1.0-ON_SQRT_EPSILON )
		  {
			  rst.x /= (r+ON_SQRT_EPSILON);
			  rst.y /= (r+ON_SQRT_EPSILON);
		  }
    }
    else if ( r > 1.0 )
	  {
		  rst.x /= r;
		  rst.y /= r;
	  }

    
    // convert to normalized texture coordinates
		rst.x = 0.5*rst.x + 0.5;
    if ( rst.x < 0.0) rst.x = 0.0; else if (rst.x > 1.0) rst.x = 1.0;
		rst.y = 0.5*rst.y + 0.5;
    if ( rst.y < 0.0) rst.y = 0.0; else if (rst.y > 1.0) rst.y = 1.0;

		if ( ON_TextureMapping::TEXTURE_SPACE::divided == m_texture_space )
		{
      // bottom uses 4/6 <= x <= 5/6 region of the texture map.
      // top uses 5/6 <= x <= 1 region of the texture map.
			rst.x = (2.0 + side0 + rst.x)/6.0;
		} 
	}
	else
	{
    // P maps to side of the cylinder.
    //
    // convert longitude to normalized texture coordinate
		t = (0.0 != rst.y || 0.0 != rst.x) ? atan2(rst.y,rst.x) : 0.0;
		rst.x = 0.5*t/ON_PI;
		if ( rst.x < -ON_EPSILON )
			rst.x += 1.0;
		else if (rst.x < 0.0 )
			rst.x = 0.0;
		else if (rst.x > 1.0 )
			rst.x = 1.0;

    if ( ON_TextureMapping::TEXTURE_SPACE::divided == m_texture_space )
    {
      // side uses 0 <= x <= 2/3 region of the texture map
      rst.x *= 2.0;
			rst.x /= 3.0;
    }

    // convert height to normalized texture coordinate
  	rst.y = 0.5*rst.z + 0.5;
    if ( m_bCapped )
    {
      // clamp height
      if ( rst.y < 0.0 ) rst.y = 0.0; else if ( rst.y > 1.0 ) rst.y = 1.0;
    }
    side0 = 1;
	}
	rst.z = r;	
	
	*T = m_uvw*rst;

  return side0;
}

int ON_TextureMapping::EvaluateBoxMapping( 
										   const ON_3dPoint& P,
										   const ON_3dVector& N,
										   ON_3dPoint* T
										   ) const
{
  // The matrix m_Pxyz transforms the world coordinate
  // "mapping cylinder" into the cylinder centered at
  // rst = (0,0,0) with radius 1.0.  The axis runs
  // from rst = (0,0,-1) to rst = (0,0,+1).

  ON_3dPoint rst(m_Pxyz*P);

	ON_3dVector n(m_Nxyz*N);
  n.Unitize();

	int side0, side1;
	double t0, t1;
	
	side0 = 0;
	t0 = 0.0;

  // side flag
  //  1 =  left side (x=-1)
  //  2 =  right side (x=+1)
  //  3 =  back side (y=-1)
  //  4 =  front side (y=+1)
  //  5 =  bottom side (z=-1)
  //  6 =  top side (z=+1)
	
  if ( ON_TextureMapping::PROJECTION::ray_projection == m_projection )
	{
		
		if ( m_bCapped )
		{
			// intersect ray with top and bottom
			side0 = IntersectBoxRayHelper(rst,n,2,&t0);
		}
		// intersect ray with front and back
		side1 = IntersectBoxRayHelper(rst,n,0,&t1);
		if ( 0 == side0 || 1 == BestHitHelper(t0,t1) )
		{
			side0 = side1;
			t0 = t1;
		}
		// intersect ray with left and right
		side1 = IntersectBoxRayHelper(rst,n,1,&t1);
		if ( 0 == side0 || 1 == BestHitHelper(t0,t1) )
		{
			side0 = side1;
			t0 = t1;
		}
		if ( 0 != side0 )
		{
			// ray hit the box
			rst = rst + t0*n;
		}
	} 

  if ( 0 == side0 )
  {
    // set side0 = side closest to the point
    side1 = (fabs(rst.x) >= fabs(rst.y)) ? 0 : 1;
    if ( m_bCapped && fabs(rst.z) > fabs(((double*)&rst.x)[side1]) )
      side1 = 2;
    t1 = (&rst.x)[side1];
    if ( t1 < 0.0 )
    {
      side0 = 2*side1 + 1;
    }
    else 
    {
      side0 = 2*side1 + 2;
    }
    
    //if ( fabs(t1) <= 1.0+ON_SQRT_EPSILON )...
    //// The point is inside the box.  If the normal
    //// is not zero, then use it to choose the side 
    //// used for the closest point projection.

    side1 = ( fabs(n.x) >= fabs(n.y) ) ? 0 : 1;
    if ( m_bCapped && fabs(n.z) > fabs((&n.x)[side1]))
    {
      side1 = 2;
    }
    t1 = n[side1];
    if ( 0.0 != t1 )
    {
      if ( t1 < 0.0 )
        side0 = 2*side1 + 1;
      else if ( t1 > 0.0 )
        side0 = 2*side1 + 2;
    }
  }

	double shift = 0.0;
	
  // side flag
  //  1 =  left side (x=-1)
  //  2 =  right side (x=+1)
  //  3 =  back side (y=-1)
  //  4 =  front side (y=+1)
  //  5 =  bottom side (z=-1)
  //  6 =  top side (z=+1)

	switch(side0)
	{
	case 1: // x = -1 
		rst.x = -rst.y; 
		rst.y =  rst.z; 
		shift =  3.0;
		break;
	case 2: // x = +1
		rst.x =  rst.y;     
		rst.y =  rst.z; 
		shift =  1.0;
		break;
	case 3: // y = -1
		rst.y =  rst.z; 
		shift =  0.0;
		break;
	case 4: // y = +1
		rst.x = -rst.x; 
		rst.y =  rst.z; 
		shift =  2.0;
		break;
	case 5: // z = -1
		rst.x = -rst.x; 
		shift =  4.0;
		break;
	case 6: // z = +1
		shift =  5.0;
		break;
	}

  // normalize texture coordinates
  rst.x = 0.5*rst.x + 0.5;
  rst.y = 0.5*rst.y + 0.5;
	rst.z = 0.0;
	
	if( ON_TextureMapping::TEXTURE_SPACE::divided == m_texture_space)
	{
    rst.x = (shift + rst.x)/(m_bCapped ? 6.0 : 4.0);
	}

	*T = m_uvw*rst;
  
  return side0;
}


int ON_TextureMapping::Evaluate(
        const ON_3dPoint& P,
        const ON_3dVector& N,
        ON_3dPoint* T,
        const ON_Xform& P_xform,
        const ON_Xform& N_xform
        ) const
{
  int rc;
  ON_3dPoint Q = P*P_xform;
  if ( ON_TextureMapping::PROJECTION::ray_projection == m_projection )
  {
    // need a transformed normal
    ON_3dVector V = N_xform*N;
    V.Unitize();
    rc = Evaluate(Q,V,T);
  }
  else
  {
    // normal is ignored
    rc = Evaluate(Q,N,T);
  }
  return rc;
}

int ON_TextureMapping::Evaluate(
        const ON_3dPoint& P,
        const ON_3dVector& N,
        ON_3dPoint* T
        ) const
{
  int rc;

	switch(m_type)
	{
	case ON_TextureMapping::TYPE::srfp_mapping:
		*T = m_uvw * P; // Do NOT apply m_Pxyz here.
    rc = 1;
		break;
	case ON_TextureMapping::TYPE::sphere_mapping:
		rc = EvaluateSphereMapping(P,N,T);
		break;
	case ON_TextureMapping::TYPE::cylinder_mapping:
		rc = EvaluateCylinderMapping(P,N,T);
		break;
	case ON_TextureMapping::TYPE::box_mapping:
		rc = EvaluateBoxMapping(P,N,T);
		break;

	case ON_TextureMapping::TYPE::mesh_mapping_primitive:
    rc = 0;
		break;

	case ON_TextureMapping::TYPE::srf_mapping_primitive:
    rc = 0;
		break;

	case ON_TextureMapping::TYPE::brep_mapping_primitive:
    rc = 0;
		break;

	default:
		rc = EvaluatePlaneMapping(P,N,T);
		break;
	}	
  return rc;
}

const ON_Object* ON_TextureMapping::CustomMappingPrimitive(void) const
{
	return m_mapping_primitive.get();
}

//Returns a valid mesh if the custom mapping primitive is a mesh.  Otherwise nullptr.
//Implementation is return ON_Mesh::Cast(CustomMappingPrimitive());
const ON_Mesh* ON_TextureMapping::CustomMappingMeshPrimitive(void) const
{
	return ON_Mesh::Cast(CustomMappingPrimitive());
}

//Returns a valid brep if the custom mapping primitive is a brep.  Otherwise nullptr.
//Implementation is return ON_Brep::Cast(CustomMappingPrimitive());
const ON_Brep* ON_TextureMapping::CustomMappingBrepPrimitive(void) const
{
	return ON_Brep::Cast(CustomMappingPrimitive());
}
//Returns a valid surface if the custom mapping primitive is a surface.  Otherwise nullptr.
//Implementation is return ON_Surface::Cast(CustomMappingPrimitive());
const ON_Surface* ON_TextureMapping::CustomMappingSurfacePrimitive(void) const
{
	return ON_Surface::Cast(CustomMappingPrimitive());
}

void ON_TextureMapping::SetCustomMappingPrimitive(ON_Object* p)
{
	m_mapping_primitive.reset(p);
}

ON__UINT32 ON_TextureMapping::MappingCRC() const
{
  // include any member that can change values returned by Evaluate
  ON__UINT32 crc32 = 0x12345678;
  crc32 = ON_CRC32(crc32,sizeof(m_type),&m_type);
  if ( ON_TextureMapping::TYPE::srfp_mapping != m_type )
  {
    // As of 21 June 2006 m_Pxyz cannot effect ON_TextureMapping::TYPE::srfp_mapping,
    // so it shouldn't be included in the CRC for srfp_mappings.
    crc32 = ON_CRC32(crc32,sizeof(m_projection),    &m_projection);
    crc32 = ON_CRC32(crc32,sizeof(m_texture_space), &m_texture_space);
    crc32 = ON_CRC32(crc32,sizeof(m_bCapped),		    &m_bCapped);
    crc32 = ON_CRC32(crc32,sizeof(m_Pxyz),          &m_Pxyz);
    // do not include m_Nxyz here - it won't help and may hurt

	  if ( m_mapping_primitive )
	  {
      switch( m_type )
      {
      case ON_TextureMapping::TYPE::mesh_mapping_primitive:
        {
          const ON_Mesh* mesh = CustomMappingMeshPrimitive();
          if ( 0 == mesh )
            break;
          crc32 = mesh->DataCRC(crc32);
          if ( mesh->HasTextureCoordinates() )
          {
            // 25 August 2010 Dale Lear
            //   Including m_T[] in crc32 per Jussi and Andy email discussion.
            //   This is probably correct because users will expect the
            //   "picture" on the mesh to be applied to the target in
            //   a visual way.
            const ON_2fPoint* tex = mesh->m_T.Array();
            crc32 = ON_CRC32(crc32,mesh->m_T.Count()*sizeof(tex[0]),tex);
          }
        }
        break;

      case ON_TextureMapping::TYPE::brep_mapping_primitive:
        {
          const ON_Brep* brep = CustomMappingBrepPrimitive();
          if ( 0 == brep )
            break;
          crc32 = brep->DataCRC(crc32);
          // 25 August 2010 Dale Lear
          //   Should brep's render meshes be included in the crc?
          //   The texture that is being mapped is actually
          //   being applied to the brep by the render mesh's
          //   m_T[] values and some users will want to see 
          //   the "picture" on the brep mapped to the 
          //   "picture" on the
          //   target.
        }
        break;

      case ON_TextureMapping::TYPE::srf_mapping_primitive:
        {
          const ON_Surface* surface = CustomMappingSurfacePrimitive();
          if ( 0 == surface )
            break;
          crc32 = surface->DataCRC(crc32);
        }
        break;

      case ON_TextureMapping::TYPE::no_mapping:
      case ON_TextureMapping::TYPE::srfp_mapping:
      case ON_TextureMapping::TYPE::plane_mapping:
      case ON_TextureMapping::TYPE::cylinder_mapping:
      case ON_TextureMapping::TYPE::sphere_mapping:
      case ON_TextureMapping::TYPE::box_mapping:
      default:
        break;
      }
    }

  }

  crc32 = ON_CRC32(crc32,sizeof(m_uvw), &m_uvw);
  return crc32;
}

bool ON_TextureMapping::RequiresVertexNormals() const
{
  if ( ON_TextureMapping::TYPE::srfp_mapping == m_type )
    return false;

	if(m_projection == ON_TextureMapping::PROJECTION::ray_projection) 
    return true;

  if(m_type == ON_TextureMapping::TYPE::box_mapping) 
    return true;
	if(m_type == ON_TextureMapping::TYPE::cylinder_mapping && m_bCapped) 
    return true;

	return false;
}

bool ON_TextureMapping::IsPeriodic(void) const
{
	return (m_type == ON_TextureMapping::TYPE::sphere_mapping || m_type == ON_TextureMapping::TYPE::cylinder_mapping);
}

bool ON_TextureMapping::HasMatchingTextureCoordinates( 
       const ON_Mesh& mesh,
       const ON_Xform* mesh_xform
       ) const
{
  bool rc = (mesh.HasTextureCoordinates())
          ? HasMatchingTextureCoordinates(mesh.m_Ttag,mesh_xform)
          : false;

  return rc;
}

bool ON_TextureMapping::HasMatchingTextureCoordinates( 
       const ON_MappingTag& tag,
       const ON_Xform* mesh_xform
       ) const
{
  bool rc = false;

  // DO NOT COMPARE m_mapping_id's in this function.
  // This function returns true if the tc values
  // calculated by the mapping will be the same
  // as the mapping that was used to set the tag.
  if ( tag.m_mapping_crc == MappingCRC() )
  {
    rc = true;

    // zero transformations indicate the mapping
    // values are independent of the 3d location
    // of the mesh.  The ON_TextureMapping::TYPE::srfp_mapping != m_type
    // check is used because these mappings are
    // alwasy independent of 3d location but
    // the transformations are often set.
    if ( ON_TextureMapping::TYPE::srfp_mapping != m_type
         && mesh_xform 
         && mesh_xform->IsValid()
         && !mesh_xform->IsZero() 
         && !tag.m_mesh_xform.IsZero()
       )
    {
      // compare xforms - these can have a bit of slop
      const double* a = &mesh_xform->m_xform[0][0];
      const double* b = &tag.m_mesh_xform.m_xform[0][0];
      for ( int i = 16; i--; /*empty*/ )
      {
        if ( fabs(*a++ - *b++) > ON_SQRT_EPSILON )
        {
          rc = false;
          break;
        }
      }
    }
  }

  return rc;
}

static
bool GetSPTCHelper(
  const ON_Mesh& mesh,
  const ON_TextureMapping& mapping,
  float* tc,
  int tc_stride
  )
{
  const int vcnt = mesh.m_V.Count();
  if ( vcnt <= 0 )
    return false;
  if ( !mesh.HasSurfaceParameters() )
    return false;
  const ON_2dPoint* S = mesh.m_S.Array();
  if ( !S )
    return false;

  int i;
  double u, v, a, b;

  // srf_udom and srf_vdom record the range
  // of parameters saved in the m_S[] array.
  ON_Interval srf_udom = mesh.m_srf_domain[0];
  ON_Interval srf_vdom = mesh.m_srf_domain[1];
  if ( !srf_udom.IsIncreasing() || !srf_vdom.IsIncreasing() )
  {
    // Attempt to calculate it from m_S[].
    srf_udom.m_t[0] = srf_udom.m_t[1] = S[0].x;
    srf_vdom.m_t[0] = srf_vdom.m_t[1] = S[0].y;
    for ( i = 1; i < vcnt; i++ )
    {
      u = S[i].x;
      if      (u < srf_udom.m_t[0]) srf_udom.m_t[0] = u; 
      else if (u > srf_udom.m_t[1]) srf_udom.m_t[1] = u; 
      v = S[i].y;
      if      (v < srf_vdom.m_t[0]) srf_vdom.m_t[0] = v; 
      else if (v > srf_vdom.m_t[1]) srf_vdom.m_t[1] = v; 
    }
    if (    !srf_udom.IsIncreasing() 
         || !srf_vdom.IsIncreasing() )
    {
      return false;
    }
  }

  bool bHaveUVWXform =   mapping.m_uvw.IsValid() 
                     && !mapping.m_uvw.IsIdentity() 
                     && !mapping.m_uvw.IsZero();

  if ( mesh.HasPackedTextureRegion() )
  {
    // Packed textures are not compatible with the use 
    // of m_uvw.  m_uvw is ignored in this block
    // of code on purpose.  //SEE BELOW
    const ON_Interval tex_udom = mesh.m_packed_tex_domain[0];
    const ON_Interval tex_vdom = mesh.m_packed_tex_domain[1];
    for ( i = 0; i < vcnt; i++)
    {
		//ALB 2011.01.14
		//Added support for m_uvw in packed textures.  Even though this conceptually makes
		//very little sense, it's one of the most requested features for the texture mapping
		//system, so I grudgingly add it.
		if (bHaveUVWXform)
		{
			const ON_2dPoint si = mapping.m_uvw*S[i];
			u = si.x;
			v = si.y;
		}
		else
		{
			u = S[i].x;
			v = S[i].y;
		}

	    // (u, v) = known surface parameter
	    if ( mesh.m_packed_tex_rotate ) 
	    {
        // verify this by checking with mesher
	       a = 1.0 - srf_vdom.NormalizedParameterAt( v );
	       b = srf_udom.NormalizedParameterAt( u );
	    }
	    else 
	    {
	      a = srf_udom.NormalizedParameterAt( u );
	      b = srf_vdom.NormalizedParameterAt( v );
	    }

      // When textures are packed, tex_udom and tex_vdom
      // are subintervals of (0,1).
	    u = tex_udom.ParameterAt(a);
	    v = tex_vdom.ParameterAt(b);

	    tc[0] = (float)u;
	    tc[1] = (float)v;
      tc += tc_stride;
    }
  }
  else if ( bHaveUVWXform )
  {
    const ON_Xform xform(mapping.m_uvw);
    ON_3dPoint P;
    for ( i = 0; i < vcnt; i++)
    {
	    // normalize surface parameter
      P.x = srf_udom.NormalizedParameterAt( S[i].x );
      P.y = srf_vdom.NormalizedParameterAt( S[i].y );
      P.z = 0.0;

      // apply m_uvw transformation
      P = xform*P;

      tc[0] = (float)P.x;
      tc[1] = (float)P.y;
      tc += tc_stride;
    }
  }
  else
  {
    // m_srf_tex_rotate is ignored on purpose.
    // It only applies if the texture is packed.
    for ( i = 0; i < vcnt; i++)
    {
	    // tc = normalized surface parameter
      a = srf_udom.NormalizedParameterAt( S[i].x );
      b = srf_vdom.NormalizedParameterAt( S[i].y );

	    tc[0] = (float)a;
	    tc[1] = (float)b;
      tc += tc_stride;
    }
  }

  return true;
}


bool ON_TextureMapping::GetTextureCoordinates(
          const ON_Mesh& mesh, 
          ON_SimpleArray<ON_3fPoint>& T,
          const ON_Xform* mesh_xform,
          bool bLazy,
          ON_SimpleArray<int>* Tside
          ) const
{
  if ( Tside )
    Tside->SetCount(0);

  int i;
  const int vcnt = mesh.m_V.Count();
  if ( vcnt <= 0 )
    return false;

  if ( bLazy )
  {
    int tci, tccount = mesh.m_TC.Count();
    for ( tci = 0; tci < tccount; tci++ )
    {
      if ( vcnt == mesh.m_TC[tci].m_T.Count() )
      {
        if ( HasMatchingTextureCoordinates(mesh.m_TC[tci].m_tag,mesh_xform) )
        {
          T = mesh.m_TC[tci].m_T;
          return true;
        }
      }
    }

    if ( HasMatchingTextureCoordinates(mesh,mesh_xform ) )
    {
      T.Reserve(vcnt);
      T.SetCount(vcnt);
      const ON_2fPoint* f = mesh.m_T.Array();
      ON_3fPoint* d = T.Array();
      for ( i = vcnt; i--; f++, d++ )
      {
        d->x = f->x;
        d->y = f->y;
        d->z = 0.0f;
      }
      return true;
    }
  }

	bool rc = false;

  if ( ON_TextureMapping::TYPE::srfp_mapping == m_type )
  {
    // uv textures from surface parameterization
    T.Reserve(vcnt);
    T.SetCount(vcnt);
    T.Zero();
    rc = GetSPTCHelper(mesh,*this,&T[0].x,3);
	}
  else
  {
    ON_3dPoint  P, tc;
		ON_3dVector N(0.0,0.0,0.0);

		const ON_3fPoint*  mesh_V = mesh.m_V.Array();
		const ON_3fVector* mesh_N = mesh.HasVertexNormals()
                              ? mesh.m_N.Array()
                              : 0;

    T.Reserve(vcnt);
    T.SetCount(vcnt);

    int* Tsd = 0;
    if ( Tside )
    {
      Tside->Reserve(vcnt);
      Tside->SetCount(vcnt);
      Tsd = Tside->Array();
      memset(Tsd,0,vcnt*sizeof(Tsd[0]));
    }

    ON_Xform P_xform(ON_Xform::IdentityTransformation), N_xform(ON_Xform::IdentityTransformation);
    const double* PT = 0;
    const double* NT = 0;
    if ( mesh_xform )
    {
      if ( mesh_xform->IsZero() || mesh_xform->IsIdentity() )
      {
        // ignore transformation
        mesh_xform = 0;
      }
      else if ( 0.0 != mesh_xform->GetMappingXforms(P_xform,N_xform) )
      {
        PT = &P_xform[0][0];
        NT = &N_xform[0][0];
      }
      else
      {
        mesh_xform = 0;
      }
    }

    const float* f;
    double w;
    int sd;

		if (ON_TextureMapping::PROJECTION::clspt_projection == m_projection 
      && (ON_TextureMapping::TYPE::mesh_mapping_primitive == m_type || ON_TextureMapping::TYPE::brep_mapping_primitive == m_type)
      && nullptr != m_mapping_primitive)
		{
      rc = false;
		}
		else if ( mesh_N &&
          (   ON_TextureMapping::PROJECTION::ray_projection == m_projection 
           || ON_TextureMapping::TYPE::box_mapping == m_type 
           || ON_TextureMapping::TYPE::cylinder_mapping == m_type
           || ON_TextureMapping::TYPE::mesh_mapping_primitive == m_type
		   )
        )
  	{
			// calculation uses mesh vertex normal
      if ( PT && NT )
      {
        // need to transform vertex and normal
        // before calculating texture coordinates
			  for (i = 0; i < vcnt; i++)
			  {
          f = &mesh_V[i].x;
				  w = PT[12]*f[0] + PT[13]*f[1] + PT[14]*f[2] + PT[15];
          w = (0.0 != w) ? 1.0/w : 1.0;
				  P.x = w*(PT[0]*f[0] + PT[1]*f[1] + PT[ 2]*f[2] + PT[ 3]);
				  P.y = w*(PT[4]*f[0] + PT[5]*f[1] + PT[ 6]*f[2] + PT[ 7]);
				  P.z = w*(PT[8]*f[0] + PT[9]*f[1] + PT[10]*f[2] + PT[11]);

          f = &mesh_N[i].x;
          N.x = PT[0]*f[0] + PT[1]*f[1] + PT[ 2]*f[2];
				  N.y = PT[4]*f[0] + PT[5]*f[1] + PT[ 6]*f[2];
				  N.z = PT[8]*f[0] + PT[9]*f[1] + PT[10]*f[2];
          N.Unitize();
				  sd = Evaluate(P,N,&tc);
				  T[i] = tc;
          if ( Tsd ) Tsd[i] = sd;
			  }
      }
			else
      {
        // mesh vertex and normal are ok
			  for (i = 0; i < vcnt; i++)
			  {
				  P = mesh_V[i];
				  N = mesh_N[i];
				  sd = Evaluate(P,N,&tc);
				  T[i] = tc;
          if ( Tsd ) Tsd[i] = sd;
			  }
      }
		}
		else if ( PT )
    {
      // normal is not used
      // mesh vertex needs to be transformed
      for ( i = 0; i < vcnt; i++ )
      {
        f = &mesh_V[i].x;
			  w = PT[12]*f[0] + PT[13]*f[1] + PT[14]*f[2] + PT[15];
        w = (0.0 != w) ? 1.0/w : 1.0;
			  P.x = w*(PT[0]*f[0] + PT[1]*f[1] + PT[ 2]*f[2] + PT[ 3]);
			  P.y = w*(PT[4]*f[0] + PT[5]*f[1] + PT[ 6]*f[2] + PT[ 7]);
			  P.z = w*(PT[8]*f[0] + PT[9]*f[1] + PT[10]*f[2] + PT[11]);
        sd = Evaluate(P,N,&tc);
			  T[i] = tc;
        if ( Tsd )
          Tsd[i] = sd;
		  }
    }
    else
		{
			// normal is not used and mesh vertex is ok
			for ( i = 0; i < vcnt; i++ )
			{
				P = mesh_V[i];
				sd = Evaluate(P,N,&tc);
				T[i] = tc;
				if ( Tsd )
					Tsd[i] = sd;
			}
    }
    rc = true;
	}

	return rc;
}

static 
void ThreeToTwoHelper( 
      const ON_SimpleArray<ON_3fPoint>& T3,
      ON_SimpleArray<ON_2fPoint>& T2
      )
{
  int i = T3.Count();
  const ON_3fPoint* t3 = T3.Array();

  T2.Reserve(i);
  T2.SetCount(i);
  ON_2fPoint* t2 = T2.Array();
  while(i--)
  {
    t2->x = t3->x;
    t2->y = t3->y;
    t2++;
    t3++;
  }
}

bool ON_TextureMapping::GetTextureCoordinates(
            const ON_Mesh& mesh, 
            ON_SimpleArray<ON_2fPoint>& T, 
            const ON_Xform* mesh_xform,
            bool bLazy,
            ON_SimpleArray<int>* Tside
            ) const
{
  bool rc = false;
  if ( Tside )
    Tside->SetCount(0);
  if ( bLazy )
  {
    if ( HasMatchingTextureCoordinates(mesh,mesh_xform ) )
    {
      if ( T.Array() != mesh.m_T.Array() )
      {
        // different arrays - copy
        T = mesh.m_T;
      }
      return true;
    }
    else
    {
      int vcnt = mesh.m_V.Count();
      int tci, tccount = mesh.m_TC.Count();
      for ( tci = 0; tci < tccount; tci++ )
      {
        if ( vcnt == mesh.m_TC[tci].m_T.Count() )
        {
          if ( HasMatchingTextureCoordinates(mesh.m_TC[tci].m_tag,mesh_xform) )
          {
            // copy T3d[] results to T[]
            ThreeToTwoHelper(mesh.m_TC[tci].m_T,T);
            return true;
          }
        }
      }
    }
  }

  if ( ON_TextureMapping::TYPE::srfp_mapping == m_type )
  {
    if (mesh.HasSurfaceParameters())
    {
      // uv textures from surface parameterization
      T.Reserve(mesh.m_V.Count());
      T.SetCount(mesh.m_V.Count());
      T.Zero();
      rc = GetSPTCHelper(mesh, *this, &T[0].x, 2);
    }
    else
    {
      //In this case, we're just going to leave the TC array in place
      rc = false;
    }
  }
  else
  {
    T.SetCount(0);
	  ON_SimpleArray<ON_3fPoint> T3;
    if ( GetTextureCoordinates(mesh, T3, mesh_xform, false, Tside ) )
    {
      // copy T3d[] results to T[]
      ThreeToTwoHelper(T3,T);
      rc = true;
	  }
  }
	return rc;
}


//bool ON_Mesh::GetSurfaceParameterTextureXform( 
//          class ON_Xform& StoT 
//          ) const
//
//{
//  bool rc = false;
//  StoT.Identity();
//
//  // Gets default mesh mapping
//  const ON_Interval surface_u_domain(m_srf_domain[0]);
//  const ON_Interval surface_v_domain(m_srf_domain[1]);
//  const ON_Interval texture_u_domain(m_tex_domain[0]);
//  const ON_Interval texture_v_domain(m_tex_domain[1]);
//  bool bRotateTexture = m_srf_tex_rotate;
//  if (   surface_u_domain.IsInterval() 
//      && surface_v_domain.IsInterval()
//      && texture_u_domain.IsInterval()
//      && texture_v_domain.IsInterval()
//      )
//  {
//    double du = 1.0/surface_u_domain.Length();
//    double dv = 1.0/surface_v_domain.Length();
//    ON_Xform x1(1.0), x2(1.0), x3(1.0);
//    x1.m_xform[0][0] = du; x1.m_xform[0][3] = -surface_u_domain[0]*du;
//    x1.m_xform[1][1] = dv; x1.m_xform[1][3] = -surface_v_domain[0]*dv;
//    if ( bRotateTexture )
//    {
//      x2.m_xform[0][0] =  0.0; x2.m_xform[0][1] = -1.0; x2.m_xform[0][3] = 1.0;
//      x2.m_xform[1][0] =  1.0; x2.m_xform[1][1] =  0.0;
//    }
//    x3.m_xform[0][0] = texture_u_domain.Length(); x3.m_xform[0][3] = texture_u_domain[0];
//    x3.m_xform[1][1] = texture_v_domain.Length(); x3.m_xform[1][3] = texture_v_domain[0];
//
//    // transforms surface(u,v) to texture(u,v)
//    StoT = x3*x2*x1;
//
//    rc = true;
//  }
//  return rc;
//}

class ON__CMeshFaceTC
{
  // DO NOT PUT THIS CLASS IN A HEADER FILE
  // IT IS A PRIVATE HELPER CLASS.
public:
  int   fi;
  int   quad[4];
  float Tx[4];
  bool  bSetT[4];
};

class ON__CChangeTextureCoordinateHelper
{
  // DO NOT PUT THIS CLASS IN A HEADER FILE
  // IT IS A PRIVATE HELPER CLASS.
public:
  ON__CChangeTextureCoordinateHelper( ON_Mesh& mesh, int newvcnt, float*& mesh_T );
  ~ON__CChangeTextureCoordinateHelper();

  int DupVertex(int vi);
  void ChangeTextureCoordinate(int* Fvi, int fvi, float x, float y, float* mesh_T, int mesh_T_stride );

  int m_tci;

  ON_Mesh& m_mesh;
  ON_3dPointArray* m_mesh_dV = nullptr;
  bool m_bHasVertexNormals;
  bool m_bHasVertexTextures;
  bool m_bHasVertexColors;
  bool m_bHasSurfaceParameters;
  bool m_bHasPrincipalCurvatures;
  bool m_bHasHiddenVertices;

  bool m_bHasCachedTextures;  
  ON_SimpleArray< ON_TextureCoordinates* > m_TC;

  // m_vuse[] is an array of length = original number of 
  // vertices in m_mesh and m_vuse[vi] = number of faces 
  // that reference vertex vi. If this vertex needs to be
  // split, vuse[vi] is decremented.  The ultimate goal
  // is to split a few times as needed so we don't
  // bloat the mesh with repeated calls to changing
  // texture maps. m_vuse[] is set the first time
  // DupVertex() is called.
  int m_vuse_count;
  ON_SimpleArray< unsigned int > m_vuse;
private:
  // no implementation
  ON__CChangeTextureCoordinateHelper(const ON__CChangeTextureCoordinateHelper&);
  ON__CChangeTextureCoordinateHelper& operator=(const ON__CChangeTextureCoordinateHelper&);
};

void ON__CChangeTextureCoordinateHelper::ChangeTextureCoordinate(int* Fvi, int fvi, float x, float y,
                                                             float* mesh_T, int mesh_T_stride )
{
  int oldvi = Fvi[fvi];
  float* T = mesh_T+(oldvi*mesh_T_stride);
  if ( x != T[0] || (y != ON_UNSET_FLOAT && y != T[1]) )
  {
    int newvi = DupVertex(oldvi);
    T = mesh_T + (newvi*mesh_T_stride);
    T[0] = x;
    if ( y != ON_UNSET_FLOAT )
     T[1] = y;

    if ( 2 == fvi && oldvi == Fvi[3] )
    {
      Fvi[2] = newvi;
      Fvi[3] = newvi;
    }
    else
    {
      Fvi[fvi] = newvi;
    }
  }
}


ON__CChangeTextureCoordinateHelper::ON__CChangeTextureCoordinateHelper( 
    ON_Mesh& mesh,
    int newvcnt,
    float*& mesh_T ) 
: m_mesh(mesh)
, m_mesh_dV(0)
, m_vuse_count(0)
{
  // adding vertices invalidates this cached information.
  m_mesh.DestroyTopology();
  m_mesh.DestroyPartition();
  m_mesh.DestroyTree();

  m_tci = -1;

  const int vcnt = m_mesh.m_V.Count();

  // It is critical to reserve enough room in the arrays
  // before duplication starts.  Otherwise, during duplication,
  // a dyanamic array can be reallocated, which will make
  // saved array base pointers will be invalid, and you crash
  // the next time they are used.

  m_mesh.m_V.Reserve(vcnt+newvcnt);

  if ( m_mesh.HasDoublePrecisionVertices() )
  {
    m_mesh_dV = &m_mesh.m_dV;
    m_mesh_dV->Reserve(vcnt+newvcnt);
  }
  else
  {
    m_mesh.DestroyDoublePrecisionVertices();
  }

  m_bHasVertexNormals = m_mesh.HasVertexNormals();
  if ( m_bHasVertexNormals ) 
    m_mesh.m_N.Reserve(vcnt+newvcnt);

  m_bHasVertexTextures = m_mesh.HasTextureCoordinates();
  if ( m_bHasVertexTextures )
  {
    float* p = (float*)m_mesh.m_T.Array();
    m_mesh.m_T.Reserve(vcnt+newvcnt);
    if ( p == mesh_T )
      mesh_T = (float*)m_mesh.m_T.Array();
  }

  m_bHasVertexColors = m_mesh.HasVertexColors();
  if ( m_bHasVertexColors )
    m_mesh.m_C.Reserve(vcnt+newvcnt);

  m_bHasSurfaceParameters = m_mesh.HasSurfaceParameters();
  if ( m_bHasSurfaceParameters )
    m_mesh.m_S.Reserve(vcnt+newvcnt);

  m_bHasPrincipalCurvatures = m_mesh.HasPrincipalCurvatures();
  if ( m_bHasPrincipalCurvatures )
    m_mesh.m_K.Reserve(vcnt+newvcnt);

  m_bHasHiddenVertices = (0 != m_mesh.HiddenVertexArray());
  if ( m_bHasHiddenVertices )
    m_mesh.m_H.Reserve(vcnt+newvcnt);

  // Set m_TC[] to be the subset of m_mesh.m_TC[] that is
  // valid for duplication.
  m_bHasCachedTextures = false;
  int tci, tccount = m_mesh.m_TC.Count();
  m_TC.Reserve(tccount);
  for ( tci = 0; tci < tccount; tci++ )
  {
    ON_TextureCoordinates& tc = m_mesh.m_TC[tci];
    if ( vcnt == tc.m_T.Count() )
    {
      m_bHasCachedTextures = true;
      float* p = (float*)tc.m_T.Array();
      tc.m_T.Reserve(vcnt+newvcnt);
      if ( p == mesh_T )
        mesh_T = (float*)tc.m_T.Array();
      m_TC.Append( &tc );
    }
  }
}


ON__CChangeTextureCoordinateHelper::~ON__CChangeTextureCoordinateHelper()
{
  if ( nullptr != m_mesh_dV )
  {
    m_mesh_dV = 0;
  }
}

int ON__CChangeTextureCoordinateHelper::DupVertex(int vi)
{
  if ( 0 == m_vuse_count )
  {
    // m_vuse[] is an array of length = original number of 
    // vertices in m_mesh and m_vuse[vi] = number of faces 
    // that reference vertex vi. If this vertex needs to be
    // split, vuse[vi] is decremented.  The ultimate goal
    // is to split a few times as needed so we don't
    // bloat the mesh with repeated calls to changing
    // texture maps. m_vuse[] is set the first time
    // DupVertex() is called.
    m_vuse_count = m_mesh.m_V.Count();
    m_vuse.Reserve(m_vuse_count);
    m_vuse.SetCount(m_vuse_count);
    m_vuse.Zero();
    for ( int fi = 0; fi < m_mesh.m_F.Count(); fi++ )
    {
      const int* Fvi = m_mesh.m_F[fi].vi;
      int i = Fvi[0];
      if ( i >= 0 && i < m_vuse_count )
        m_vuse[i]++;
      i = Fvi[1];
      if ( i >= 0 && i < m_vuse_count )
        m_vuse[i]++;
      i = Fvi[2];
      if ( i >= 0 && i < m_vuse_count )
        m_vuse[i]++;
      i = Fvi[3];
      if ( Fvi[2] != i && i >= 0 && i < m_vuse_count )
        m_vuse[i]++;
    }
  }

  if ( vi >= 0 && vi < m_vuse_count )
  {
    if ( m_vuse[vi] <= 1 )
      return vi; // only one face uses this vertex - no need to dup the vertex

    // otherwise we will duplicate this vertex, reducing its use count by 1.
    m_vuse[vi]--;
  }


  m_mesh.m_V.AppendNew();
  *m_mesh.m_V.Last() = m_mesh.m_V[vi];
  if ( 0 != m_mesh_dV )
  {
    m_mesh_dV->AppendNew();
    *(m_mesh_dV->Last()) = m_mesh_dV->operator[](vi);
  }
  if ( m_bHasVertexTextures )
  {
    m_mesh.m_T.AppendNew();
    *m_mesh.m_T.Last() = m_mesh.m_T[vi];
  }
  if ( m_bHasVertexNormals )
  {
    m_mesh.m_N.AppendNew();
    *m_mesh.m_N.Last() = m_mesh.m_N[vi];
  }
  if ( m_bHasVertexColors )
  {
    m_mesh.m_C.AppendNew();
    *m_mesh.m_C.Last() = m_mesh.m_C[vi];
  }
  if ( m_bHasSurfaceParameters )
  {
    m_mesh.m_S.AppendNew();
    *m_mesh.m_S.Last() = m_mesh.m_S[vi];
  }
  if ( m_bHasPrincipalCurvatures )
  {
    m_mesh.m_K.AppendNew();
    *m_mesh.m_K.Last() = m_mesh.m_K[vi];
  }
  if ( m_bHasHiddenVertices )
  {
    m_mesh.m_H.AppendNew();
    if ( 0 != (*m_mesh.m_H.Last() = m_mesh.m_H[vi]) )
      m_mesh.m_hidden_count++;
  }

  if ( m_bHasCachedTextures )
  {
    // Note:  This m_TC[] is the subset of m_mesh.m_TC[]
    //        that need to be duped.  The constructor
    //        insures that m_TC[i] is not nullptr and
    //        has the right count and capacity.
    //
    //        DO NOT REFERENCE m_mesh.m_TC[] in this block.
    int tccount = m_TC.Count();
    for ( int i = 0; i < tccount; i++ )
    {
      ON_SimpleArray<ON_3fPoint>& T = m_TC[i]->m_T;
      T.AppendNew();
      *T.Last() = T[vi];
    }
  }

  return m_mesh.m_V.Count()-1;
}


static
float PoleFix( float t0,  float t1 )
{
  float t = ( ON_UNSET_FLOAT == t0 )
          ? t1
          : ((ON_UNSET_FLOAT == t1 ) ? t0 : (0.5f*(t0+t1)));
  return t;
}

static
int IntersectBoxSideRayHelper(int side, const ON_3dPoint& rst, const ON_3dVector& n, double* s)
{
  /*
  returns:
    0 = ray parallel to sides
    1 = ray hit left side (x=-1)
    2 = ray hit right side (x=+1)
    3 = ray hit back side (y=-1)
    4 = ray hit front side (y=+1)
    5 = ray hit bottom side (z=-1)
    6 = ray hit top side (z=+1)
  */
  double nx;
  ON_3dPoint Q;
  double t,t0,t1;
  int dir;


  switch(side)
  {
  case 1: // =  left side (x=-1)
    t1 = -1.0;
    dir = 0;
    break;
  case 2: //   right side (x=+1)
    t1 = 1.0;
    dir = 0;
    break;
  case 3: //   back side (y=-1)
    t1 = -1.0;
    dir = 1;
    break;
  case 4: //   front side (y=+1)
    t1 = 1.0;
    dir = 1;
    break;
  case 5: //   bottom side (z=-1)
    t1 = -1.0;
    dir = 2;
    break;
  case 6: //   top side (z=+1)
    t1 = 1.0;
    dir = 2;
    break;
  default:
    *s = ON_UNSET_VALUE;
    return 0;
    break;
  }

  // protect against overflow
  nx = (&n.x)[dir];
  t0 = (t1 - (&rst.x)[dir]);
  if ( fabs(t0) >= fabs(nx)*on__overflow_tol )
  {
    *s = ON_UNSET_VALUE;
    return 0;
  }

  t0 /= nx;
  Q = rst + t0*n;
  if ( dir )
  {
    t = Q.x;
    Q.x = Q[dir];
    Q[dir] = t;
  }
  if ( fabs(Q.x-t1) > ON_SQRT_EPSILON || fabs(Q.y) > 1.0e8 || fabs(Q.z) > 1.0e8 )
  {
    *s = ON_UNSET_VALUE;
    return 0;
  }


  *s = t0;
  return side;
}

static
bool EvBoxSideTextureCoordinateHelper2( 
                       int side,
                       const ON_TextureMapping& box_mapping,
										   const ON_3dPoint& P,
										   const ON_3dVector& N,
										   ON_3dPoint* T
										   )
{
  // side flag
  //  1 =  left side (x=-1)
  //  2 =  right side (x=+1)
  //  3 =  back side (y=-1)
  //  4 =  front side (y=+1)
  //  5 =  bottom side (z=-1)
  //  6 =  top side (z=+1)
  // The matrix m_Pxyz transforms the world coordinate
  // "mapping cylinder" into the cylinder centered at
  // rst = (0,0,0) with radius 1.0.  The axis runs
  // from rst = (0,0,-1) to rst = (0,0,+1).

  ON_3dPoint rst(box_mapping.m_Pxyz*P);

	ON_3dVector n(box_mapping.m_Nxyz*N);
  n.Unitize();

  // side flag
  //  1 =  left side (x=-1)
  //  2 =  right side (x=+1)
  //  3 =  back side (y=-1)
  //  4 =  front side (y=+1)
  //  5 =  bottom side (z=-1)
  //  6 =  top side (z=+1)
	
  if ( ON_TextureMapping::PROJECTION::ray_projection == box_mapping.m_projection )
	{
    double s;
    if ( side == IntersectBoxSideRayHelper(side, rst, n, &s) )
    {
		  // ray hit the box side
		  rst = rst + s*n;
    }
	} 

	double shift = 0.0;
	
  // side flag
  //  1 =  left side (x=-1)
  //  2 =  right side (x=+1)
  //  3 =  back side (y=-1)
  //  4 =  front side (y=+1)
  //  5 =  bottom side (z=-1)
  //  6 =  top side (z=+1)

	switch(side)
	{
	case 1: // x = -1 
		rst.x = -rst.y; 
		rst.y =  rst.z; 
		shift =  3.0;
		break;
	case 2: // x = +1
		rst.x =  rst.y;     
		rst.y =  rst.z; 
		shift =  1.0;
		break;
	case 3: // y = -1
		rst.y =  rst.z; 
		shift =  0.0;
		break;
	case 4: // y = +1
		rst.x = -rst.x; 
		rst.y =  rst.z; 
		shift =  2.0;
		break;
	case 5: // z = -1
		rst.x = -rst.x; 
		shift =  4.0;
		break;
	case 6: // z = +1
		shift =  5.0;
		break;
  default:
    return 0;
    break;
	}

  // normalize texture coordinates
  rst.x = 0.5*rst.x + 0.5;
  rst.y = 0.5*rst.y + 0.5;
	rst.z = 0.0;
	
	if( ON_TextureMapping::TEXTURE_SPACE::divided == box_mapping.m_texture_space)
	{
    rst.x = (shift + rst.x)/(box_mapping.m_bCapped ? 6.0 : 4.0);
	}

	*T = box_mapping.m_uvw*rst;
  
  return true;
}

static
bool EvBoxSideTextureCoordinateHelper1(
          const ON_Mesh& mesh, 
          const ON_Xform* mesh_xform,
          int vi,
          int side,
          const ON_TextureMapping& box_mapping,
          float* Tx,
          float* Ty
          )
{
	bool rc = false;
  ON_3dPoint  P, tc;
	ON_3dVector N(0.0,0.0,0.0);

	const ON_3fPoint*  mesh_V = mesh.m_V.Array();
	const ON_3fVector* mesh_N = mesh.HasVertexNormals()
                            ? mesh.m_N.Array()
                            : 0;

  ON_Xform P_xform(ON_Xform::IdentityTransformation), N_xform(ON_Xform::IdentityTransformation);
  const double* PT = 0;
  const double* NT = 0;
  if ( mesh_xform )
  {
    if ( mesh_xform->IsZero() || mesh_xform->IsIdentity() )
    {
      // ignore transformation
      mesh_xform = 0;
    }
    else if ( 0.0 != mesh_xform->GetMappingXforms(P_xform,N_xform) )
    {
      PT = &P_xform[0][0];
      NT = &N_xform[0][0];
    }
    else
    {
      mesh_xform = 0;
    }
  }

  const float* f;
  double w;

  if ( mesh_N && ON_TextureMapping::PROJECTION::ray_projection == box_mapping.m_projection )
	{
		// calculation uses mesh vertex normal
    if ( PT && NT )
    {
      // need to transform vertex and normal
      // before calculating texture coordinates
      f = &mesh_V[vi].x;
		  w = PT[12]*f[0] + PT[13]*f[1] + PT[14]*f[2] + PT[15];
      w = (0.0 != w) ? 1.0/w : 1.0;
		  P.x = w*(PT[0]*f[0] + PT[1]*f[1] + PT[ 2]*f[2] + PT[ 3]);
		  P.y = w*(PT[4]*f[0] + PT[5]*f[1] + PT[ 6]*f[2] + PT[ 7]);
		  P.z = w*(PT[8]*f[0] + PT[9]*f[1] + PT[10]*f[2] + PT[11]);

      f = &mesh_N[vi].x;
      N.x = PT[0]*f[0] + PT[1]*f[1] + PT[ 2]*f[2];
		  N.y = PT[4]*f[0] + PT[5]*f[1] + PT[ 6]*f[2];
		  N.z = PT[8]*f[0] + PT[9]*f[1] + PT[10]*f[2];
      N.Unitize();
    }
    else
    {
      // mesh vertex and normal are ok
		  P = mesh_V[vi];
		  N = mesh_N[vi];
    }
	}
	else if ( PT )
  {
    // normal is not used
    // mesh vertex needs to be transformed
    f = &mesh_V[vi].x;
	  w = PT[12]*f[0] + PT[13]*f[1] + PT[14]*f[2] + PT[15];
    w = (0.0 != w) ? 1.0/w : 1.0;
	  P.x = w*(PT[0]*f[0] + PT[1]*f[1] + PT[ 2]*f[2] + PT[ 3]);
	  P.y = w*(PT[4]*f[0] + PT[5]*f[1] + PT[ 6]*f[2] + PT[ 7]);
	  P.z = w*(PT[8]*f[0] + PT[9]*f[1] + PT[10]*f[2] + PT[11]);
  }
  else
  {
    // normal is not used and mesh vertex is ok
    P = mesh_V[vi];
  }


  rc = EvBoxSideTextureCoordinateHelper2(side,box_mapping,P,N,&tc);
  if (rc)
  {
    rc = tc.IsValid();
    if (rc)
    {
      *Tx = (float)tc.x;
      *Ty = (float)tc.y;
    }
  }
	return rc;
}


class ON__CNewMeshFace
{
public:
  int fi;
  int newvcnt;
  bool bNewV[4];
  ON_2fPoint tc[4];
};

static
float TcDistanceHelper(const ON_2fPoint& tc)
{
  float dx = (tc.x > 0.5f) ? (1.0f-tc.x) : tc.x;
  if ( dx < 0.0f) 
    return 0.0f;
  float dy = (tc.y > 0.5f) ? (1.0f-tc.y) : tc.y;
  if ( dy < 0.0f) 
    return 0.0f;
  return (dx < dy) ? dx : dy;
}

static
void AdjustSingleBoxTextureCoordinatesHelper( 
          ON_Mesh& mesh, 
          const ON_Xform* mesh_xform,
          float* mesh_T,
          int    mesh_T_stride,
          const int* Tsd,
          const ON_TextureMapping& box_mapping
          )
{
  const int vcnt = mesh.m_V.Count();
  const int fcnt = mesh.m_F.Count();
  if ( vcnt < 3 || fcnt < 1 || vcnt != mesh.m_T.Count() || !Tsd )
    return;
  const ON_MeshFace* mesh_F = mesh.m_F.Array();
  const int* Fvi;
  int j, k, fi, sd[4], fvicnt, side, newvcnt=0;
  ON__CNewMeshFace mf;
  ON_2fPoint tc;
  ON_SimpleArray<ON__CNewMeshFace> mflist(512);
  float d;
  for ( fi = 0; fi < fcnt; fi++ )
  {
    Fvi = mesh_F[fi].vi;
    sd[0] = Tsd[Fvi[0]];
    sd[1] = Tsd[Fvi[1]];
    sd[2] = Tsd[Fvi[2]];
    sd[3] = Tsd[Fvi[3]];
    if ( sd[0] == sd[1] && sd[0] == sd[2] && sd[0] == sd[3] )
    {
      // all texture coords are on same side of box
      continue;
    }
    fvicnt = (Fvi[2] != Fvi[3]) ? 4 : 3;

    memset(&mf,0,sizeof(mf));
    mf.tc[0] = mesh_T + (Fvi[0]*mesh_T_stride);
    mf.tc[1] = mesh_T + (Fvi[1]*mesh_T_stride);
    mf.tc[2] = mesh_T + (Fvi[2]*mesh_T_stride);
    mf.tc[3] = mesh_T + (Fvi[3]*mesh_T_stride);

    // find the side we will use for this face
    side = sd[0];
    d = TcDistanceHelper(mf.tc[0]);
    for ( j = 1; j < fvicnt; j++ )
    {
      float d1 = TcDistanceHelper(mf.tc[j]);
      if (d1 > d)
      {
        side = sd[j];
        d = d1;
      }
    }

    // Jussi, 5th September 2011:
    // This 'continue' only works for faces having one or more of its tc's in (0,1)x(0,1).
    // I have commented it out as a fix to RR 90329.
    //if ( d <= 0.0f )
    //  continue;

    for ( j = 0; j < fvicnt; j++ )
    {
      if ( sd[j] != side )
      {
        // calculate new tc for this side
        if ( EvBoxSideTextureCoordinateHelper1(
          mesh,
          mesh_xform,
          Fvi[j],
          side,
          box_mapping,
          &tc.x,&tc.y) )
        {
          if ( tc.x != mf.tc[j].x || tc.y != mf.tc[j].y )
          {
            mf.tc[j] = tc;
            mf.bNewV[j] = true;
            mf.newvcnt++;
          }
        }
        else
          break;
      }
    }
    if ( j >= fvicnt && mf.newvcnt > 0 )
    {
      mf.fi = fi;
      newvcnt += mf.newvcnt;
      mflist.Append(mf);
    }
  }

  if ( newvcnt <= 0 )
    return;

  ON__CChangeTextureCoordinateHelper helper(mesh,vcnt+newvcnt,mesh_T);
  
  const int mflist_count = mflist.Count();

  for ( k = 0; k < mflist_count; k++ )
  {
    mf = mflist[k];
    int* fvi = mesh.m_F[mf.fi].vi;
    fvicnt = (fvi[2]!=fvi[3]) ? 4 : 3;
    for ( j = 0; j < fvicnt; j++ )
    {
      if ( mf.bNewV[j] )
      {
        helper.ChangeTextureCoordinate(fvi,j,mf.tc[j].x,mf.tc[j].y,mesh_T,mesh_T_stride);
      }
    }    
  }
}

static 
void AdjustMeshPeriodicTextureCoordinatesHelper( 
          ON_Mesh& mesh, 
          const ON_Xform* mesh_xform,
          float* mesh_T,
          int    mesh_T_stride,
          const int* Tsd,
          double two_pi_tc,
          const ON_TextureMapping& mapping
          )
{
  // This helper adjusts texture coordinates on faces that
  // span the seam on mapping spheres and cylinders and
  // resolves the mulitiple valued problem that
  // exists at the poles of sphere mappings.

  const int vcnt = mesh.m_V.Count();
  const int fcnt = mesh.m_F.Count();
  if ( vcnt < 3 || fcnt < 1 || vcnt != mesh.m_T.Count() )
    return;

  // see if any texture coordinate adjustment is necessary
  const ON_TextureMapping::TYPE mapping_type = mapping.m_type;
  const bool bSphereCheck = ( ON_TextureMapping::TYPE::sphere_mapping == mapping_type );
  const bool bCylinderCheck = (Tsd && ON_TextureMapping::TYPE::cylinder_mapping == mapping_type);
  const bool bBoxCheck = (Tsd && ON_TextureMapping::TYPE::box_mapping == mapping_type);

  if ( bBoxCheck && ON_TextureMapping::TEXTURE_SPACE::single == mapping.m_texture_space )
  {
    AdjustSingleBoxTextureCoordinatesHelper( mesh, mesh_xform, mesh_T, mesh_T_stride, Tsd, mapping );
    return;
  }

  ON_Workspace ws;
  int* quad = ws.GetIntMemory(vcnt); // ~ws will free quad memory
  float* Tx = (float*)ws.GetMemory(vcnt*sizeof(Tx[0]));
  float t;
  int vi, ti, q=0;
  int ftc_count = 0;

  const float ang0 = (float)(0.25*two_pi_tc);
  const float ang1 = (float)(0.75*two_pi_tc);


  for ( vi = ti = 0; vi < vcnt; vi++, ti += mesh_T_stride )
  {
    quad[vi] = 0;
    Tx[vi] = mesh_T[ti];
    if ( bCylinderCheck )
    {
      if ( 1 != Tsd[vi] )
        continue;
    }
    else if ( bBoxCheck )
    {
      if ( 1 != Tsd[vi] && 3 != Tsd[vi] )
        continue;
    }
    else if ( bSphereCheck )
    {
      t = mesh_T[ti+1]; // t = "v" texture coordinate
      if ( t < 0.001f )
      {
        quad[vi] = 8; q |= 8; // south pole point
        ftc_count++;
        continue;
      }
      if ( t > 0.999f )
      {
        quad[vi] = 8; q |= 8; // north pole point
        ftc_count++;
        continue;
      }
    }

    t = Tx[vi]; // t = "u" texture coordinate
    if ( t < ang0 )
    {      
      quad[vi] = 1; q |= 1; // longitude < pi/2
      ftc_count++;
    }
    else if ( t > ang1 )
    {
      quad[vi] = 4; q |= 4; // longitude > 3pi/2
      ftc_count++;
    }
  }

  if ( 0 == q || 1 == q || 4 == q )
  {
    // nothing needs to be adjusted
    return;
  }

  // 4*ftc_count = (over) estimate of the number of faces that
  // will be changed.
  ON_SimpleArray<ON__CMeshFaceTC> ftc_list(ftc_count*4 + 128);
  ftc_count = 0;
  const ON_MeshFace* F = mesh.m_F.Array();
  const int* Fvi;
  int fi;
  ON__CMeshFaceTC ftc;
  memset(&ftc,0,sizeof(ftc));
  float t0, t1;

  for ( fi = 0; fi < fcnt; fi++ )
  {
    Fvi = F[fi].vi;

    ftc.quad[0] = quad[Fvi[0]];
    ftc.quad[1] = quad[Fvi[1]];
    ftc.quad[2] = quad[Fvi[2]];
    ftc.quad[3] = quad[Fvi[3]];

    q = (ftc.quad[0] | ftc.quad[1] | ftc.quad[2] | ftc.quad[3]);
    if ( 0 == q || 1 == q || 4 == q )
    {
      // no adjustments need to be made
      continue;
    }

    // ftc.fi will be set to fi if a texture coordinate needs to be adjusted
    ftc.fi = -1; 

    ftc.Tx[0] = Tx[Fvi[0]];
    ftc.Tx[1] = Tx[Fvi[1]];
    ftc.Tx[2] = Tx[Fvi[2]];
    ftc.Tx[3] = Tx[Fvi[3]];

    if ( 0 != (8&q) )
    {
      // see if check for north/south sphere mapping poles and fix them
      if ( 8 == ftc.quad[0] ) 
      {
        t0 = (8 == ftc.quad[3]) ? ON_UNSET_FLOAT : ftc.Tx[3];
        t1 = (8 == ftc.quad[1]) ? ON_UNSET_FLOAT : ftc.Tx[1];
        if ( ON_UNSET_FLOAT != t0 || ON_UNSET_FLOAT != t1 )
        {
          ftc.Tx[0] = PoleFix(t0,t1);
          ftc.quad[0] = ((ftc.Tx[0] < ang0) ? 1 : ((ftc.Tx[0] > ang1) ? 4 : 0));
          q |= ftc.quad[0];
          ftc.fi = fi;
        }
      }
      if ( 8 == ftc.quad[1] ) 
      {
        t0 = (8 == ftc.quad[0]) ? ON_UNSET_FLOAT : ftc.Tx[0];
        t1 = (8 == ftc.quad[2]) ? ON_UNSET_FLOAT : ftc.Tx[2];
        if ( ON_UNSET_FLOAT != t0 || ON_UNSET_FLOAT != t1 )
        {
          ftc.Tx[1] = PoleFix(t0,t1);
          ftc.quad[1] = ((ftc.Tx[1] < ang0) ? 1 : ((ftc.Tx[1] > ang1) ? 4 : 0));
          q |= ftc.quad[1];
          ftc.fi = fi;
        }
      }
      if ( 8 == ftc.quad[2] ) 
      {
        int k = (Fvi[2] == Fvi[3]) ? 0 : 3;
        t0 = (8 == ftc.quad[1]) ? ON_UNSET_FLOAT : ftc.Tx[1];
        t1 = (8 == ftc.quad[k]) ? ON_UNSET_FLOAT : ftc.Tx[k];
        if ( ON_UNSET_FLOAT != t0 || ON_UNSET_FLOAT != t1 )
        {
          ftc.Tx[2] = PoleFix(t0,t1);
          ftc.quad[2] = ((ftc.Tx[2] < ang0) ? 1 : ((ftc.Tx[2] > ang1) ? 4 : 0));
          if ( !k )
          {
            ftc.Tx[3] = ftc.Tx[2];
            ftc.quad[3] = ftc.quad[2];
          }
          q |= ftc.quad[2];
          ftc.fi = fi;
        }
      }
      if ( 8 == ftc.quad[3] && Fvi[2] != Fvi[3] ) 
      {
        t0 = (8 == ftc.quad[2]) ? ON_UNSET_FLOAT : ftc.Tx[2];
        t1 = (8 == ftc.quad[0]) ? ON_UNSET_FLOAT : ftc.Tx[0];
        if ( ON_UNSET_FLOAT != t0 || ON_UNSET_FLOAT != t1 )
        {
          ftc.Tx[3] = PoleFix(t0,t1);
          ftc.quad[3] = ((ftc.Tx[3] < ang0) ? 1 : ((ftc.Tx[3] > ang1) ? 4 : 0));
          q |= ftc.quad[3];
          ftc.fi = fi;
        }
      }
    }

    if ( 5 == (5&q) )
    {
      // The face has corners on both sides of the seam
      if ( two_pi_tc == 1.0 )
      {
        if ( 1 == ftc.quad[0] ) {ftc.Tx[0] += 1.0f; ftc.fi = fi;}
        if ( 1 == ftc.quad[1] ) {ftc.Tx[1] += 1.0f; ftc.fi = fi;}
        if ( 1 == ftc.quad[2] ) {ftc.Tx[2] += 1.0f; ftc.fi = fi;}
        if ( 1 == ftc.quad[3] ) {ftc.Tx[3] += 1.0f; ftc.fi = fi;}
      }
      else
      {
        // With divided textures, wrapping the texture coordinate
        // does not work because it wraps into a region of the
        // texture not use by this "side".  In this case, the
        // only thing to do is to pick the best end of the texture
        // map and clamp the tcs that hang over.  If the mesh
        // has edges near the texture seam, the picture will
        // still look ok.
        float f0=0.0f, f1=0.0f, twopitc = (float)two_pi_tc;;
        //int f0cnt=0, f1cnt=0;
        if ( 1 == ftc.quad[0] ) f0 += ftc.Tx[0]; else if ( 4 == ftc.quad[0] ) f1 += twopitc-ftc.Tx[0];
        if ( 1 == ftc.quad[1] ) f0 += ftc.Tx[1]; else if ( 4 == ftc.quad[1] ) f1 += twopitc-ftc.Tx[1];
        if ( 1 == ftc.quad[2] ) f0 += ftc.Tx[2]; else if ( 4 == ftc.quad[2] ) f1 += twopitc-ftc.Tx[2];
        if (Fvi[2] != Fvi[3])
        {
          if ( 1 == ftc.quad[3] ) f0 += ftc.Tx[3]; else if ( 4 == ftc.quad[3] ) f1 += twopitc-ftc.Tx[3];
        }
        if (f0 >= f1 )
        {
          // "most" of the face is on the left side of the texture 
          // If a vertex is on the right side, clamp its tc to 0.
          if ( 4 == ftc.quad[0] ) {ftc.Tx[0] = 0.0f; ftc.fi = fi;}
          if ( 4 == ftc.quad[1] ) {ftc.Tx[1] = 0.0f; ftc.fi = fi;}
          if ( 4 == ftc.quad[2] ) {ftc.Tx[2] = 0.0f; ftc.fi = fi;}
          if ( 4 == ftc.quad[3] ) {ftc.Tx[3] = 0.0f; ftc.fi = fi;}
        }
        else
        {
          // "most" of the face is on the right side of the texture 
          // If a vertex is on the left side, clamp its tc to two_pi_tc.
          if ( 1 == ftc.quad[0] ) {ftc.Tx[0] = twopitc; ftc.fi = fi;}
          if ( 1 == ftc.quad[1] ) {ftc.Tx[1] = twopitc; ftc.fi = fi;}
          if ( 1 == ftc.quad[2] ) {ftc.Tx[2] = twopitc; ftc.fi = fi;}
          if ( 1 == ftc.quad[3] ) {ftc.Tx[3] = twopitc; ftc.fi = fi;}
        }
      }
    }

    if ( ftc.fi >= 0 )
    {
      // face will require special handling
      ftc_list.Append(ftc);    
    }
  }

  ftc_count = ftc_list.Count();
  if ( ftc_count <= 0 )
    return;

  // Count the number of new vertices that will be added.
  int ftci;
  int newvcnt = 0;
  for ( ftci = 0; ftci < ftc_count; ftci++ )
  {
    ON__CMeshFaceTC& ftc_local = ftc_list[ftci];
    Fvi = F[ftc_local.fi].vi;
    if ( ftc_local.Tx[0] != Tx[Fvi[0]] )
    {
      ftc_local.bSetT[0] = true;
      newvcnt++;
    }
    if ( ftc_local.Tx[1] != Tx[Fvi[1]] )
    {
      ftc_local.bSetT[1] = true;
      newvcnt++;
    }
    if ( ftc_local.Tx[2] != Tx[Fvi[2]] )
    {
      ftc_local.bSetT[2] = true;
      newvcnt++;
    }
    if ( Fvi[2] != Fvi[3] )
    {
      if ( ftc_local.Tx[3] != Tx[Fvi[3]] )
      {
        ftc_local.bSetT[3] = true;
        newvcnt++;
      }
    }
  }

  if ( newvcnt <= 0 )
    return;


  F = 0; // Setting them to nullptr makes sure anybody who
         // tries to use them below will crash.

  // reserve room for new vertex information
  ON__CChangeTextureCoordinateHelper helper(mesh,newvcnt,mesh_T);

  // add vertices and update mesh faces
  for ( ftci = 0; ftci < ftc_count; ftci++ )
  {
    const ON__CMeshFaceTC& ftc_local = ftc_list[ftci];
    int* meshFvi = mesh.m_F[ftc_local.fi].vi;

    if ( ftc_local.bSetT[0] )
    {
      helper.ChangeTextureCoordinate(meshFvi,0,ftc_local.Tx[0],ON_UNSET_FLOAT,mesh_T,mesh_T_stride);
    }
    if ( ftc_local.bSetT[1] )
    {
      helper.ChangeTextureCoordinate(meshFvi,1,ftc_local.Tx[1],ON_UNSET_FLOAT,mesh_T,mesh_T_stride);
    }
    if ( ftc_local.bSetT[2] )
    {
      helper.ChangeTextureCoordinate(meshFvi,2,ftc_local.Tx[2],ON_UNSET_FLOAT,mesh_T,mesh_T_stride);
    }
    if ( ftc_local.bSetT[3] )
    {
      helper.ChangeTextureCoordinate(meshFvi,3,ftc_local.Tx[3],ON_UNSET_FLOAT,mesh_T,mesh_T_stride);
    }
  }
}

static
bool SeamCheckHelper( const ON_TextureMapping& mp, 
                      double& two_pi_tc, 
                      ON_SimpleArray<int>& Tside,
                      ON_SimpleArray<int>*& Tsd )
{
  bool bSeamCheck = false;
  switch(mp.m_type)
  {
    case ON_TextureMapping::TYPE::box_mapping:
      if ( ON_TextureMapping::TEXTURE_SPACE::divided == mp.m_texture_space )
      {
        if ( mp.m_bCapped )
          two_pi_tc = 2.0/3.0;
        Tsd = &Tside;
        bSeamCheck = true;
      }
      else if ( ON_TextureMapping::TEXTURE_SPACE::single == mp.m_texture_space )
      {
        Tsd = &Tside;
        bSeamCheck = true;
      }
      break;

    case ON_TextureMapping::TYPE::cylinder_mapping:
      if ( ON_TextureMapping::TEXTURE_SPACE::divided == mp.m_texture_space )
      {
        two_pi_tc = 2.0/3.0;
        Tsd = &Tside;
      }
      bSeamCheck = true;
      break;

    case ON_TextureMapping::TYPE::sphere_mapping:
      bSeamCheck = true;
      break;

    default:
      // intentionally skip other enum values
      break;
  }

  return bSeamCheck;
}

//If there are unused vertices, this may not work correctly - but it is very fast.
static inline bool HasSharedVertices(const ON_Mesh& mesh)
{
  return mesh.m_V.Count() < ((mesh.TriangleCount() * 3) + (mesh.QuadCount() * 4));
}


const ON_TextureCoordinates* ON_Mesh::SetCachedTextureCoordinates( 
        const class ON_TextureMapping& mapping,
				const class ON_Xform* mesh_xform,
        bool bLazy
        )
{
  if ( mapping.RequiresVertexNormals() && !HasVertexNormals() )
    ComputeVertexNormals();

  ON_TextureMapping mp = mapping;
  double two_pi_tc = 1.0;
  ON_SimpleArray<int> Tside;
  ON_SimpleArray<int>* Tsd = 0;
  bool bSeamCheck = SeamCheckHelper( mp, two_pi_tc, Tside, Tsd ) && HasSharedVertices(*this);
  if ( bSeamCheck )
    mp.m_uvw = ON_Xform::IdentityTransformation;

  ON_TextureCoordinates* TC = 0;
  {
    for ( int i = 0; i < m_TC.Count(); i++ )
    {
      if ( m_TC[i].m_tag.m_mapping_id == mapping.Id() )
      {
        TC = &m_TC[i];
        break;
      }
    }
  }
  if ( bLazy && TC && mapping.HasMatchingTextureCoordinates( TC->m_tag, mesh_xform ) )
    return TC;

  if ( !TC )
  {
    m_TC.AppendNew();
    TC = m_TC.Last();
  }

  // Use mp instead of mapping to call GetTextureCoordinates()
  // because m_uvw must be the identity if we have seams.
  if ( !mp.GetTextureCoordinates( *this,TC->m_T,mesh_xform,false,Tsd) )
  {
    int tci = (int)(TC - m_TC.Array());
    m_TC.Remove(tci);
    return 0;
  }

  TC->m_tag.Set(mapping);
  if (    mesh_xform && mesh_xform->IsValid()
       && !mesh_xform->IsIdentity() 
       && !mesh_xform->IsZero()
     )
  {
    TC->m_tag.m_mesh_xform = *mesh_xform;
  }

  TC->m_dim = 2;

  if ( bSeamCheck &&  m_F.Count() > 0 && TC->m_T.Count() == m_V.Count() )
  {
    float* mesh_T = (float*)TC->m_T.Array();
    int mesh_T_stride = sizeof(TC->m_T[0])/sizeof(mesh_T[0]);
    if ( Tsd && Tside.Count() != m_V.Count() )
      Tsd = 0;
    AdjustMeshPeriodicTextureCoordinatesHelper( *this, mesh_xform, mesh_T, mesh_T_stride, Tsd ? Tside.Array() : 0, two_pi_tc, mp );
    mesh_T = 0; // when the array is grown, the pointer may become invalid
    if ( !mapping.m_uvw.IsIdentity() && !mapping.m_uvw.IsZero() )
    {
      // Apply the uvw transformation that is on mapping
      // to the texture coordinates.
      ON_3dPoint T;
      int vi, vcnt = TC->m_T.Count();
      ON_3fPoint* meshT = TC->m_T.Array();
      for ( vi = 0; vi < vcnt; vi++ )
      {
        T = meshT[vi];
        T = mapping.m_uvw*T;
        meshT[vi] = T;
      }
    }
  }

  return TC;
}

bool ON_Mesh::SetTextureCoordinates(
                  const class ON_TextureMapping& mapping, 
                  const class ON_Xform* mesh_xform,
                  bool bLazy
                  )
{
  if ( mapping.RequiresVertexNormals() && !HasVertexNormals() )
    ComputeVertexNormals();

  InvalidateTextureCoordinateBoundingBox();

  ON_SimpleArray<int> Tside;
  ON_SimpleArray<int>* Tsd = 0;
  ON_TextureMapping mp = mapping;
  
  double two_pi_tc = 1.0;

  bool bSeamCheck = SeamCheckHelper( mp, two_pi_tc, Tside, Tsd ) && HasSharedVertices(*this);
  if ( bSeamCheck )
    mp.m_uvw = ON_Xform::IdentityTransformation;

  // Use mp instead of mapping to call GetTextureCoordinates()
  // because m_uvw must be the identity if we have seams.
  bool rc = mp.GetTextureCoordinates(*this,m_T,mesh_xform,bLazy,Tsd);

  if (Tsd != nullptr && Tsd->Count() == 0)
  {
    // Tsd array is needed for seam check but it was not filled by GetTextureCoordinates.
    // This happened because matching texture coordinates were found. These coordinates
    // were already once seam checked. So seam check can be skipped now.
    bSeamCheck = false;
  }
  
  if (rc)
  {
    // update the texture coordinate tag
    m_Ttag.Set(mapping);
    if (    mesh_xform 
         && mesh_xform->IsValid() 
         && !mesh_xform->IsIdentity() 
         && !mesh_xform->IsZero() 
       )
    {
      m_Ttag.m_mesh_xform  = *mesh_xform;
    }
  }

  if ( rc && bSeamCheck && HasTextureCoordinates() && m_F.Count() > 0 )
  {
    float* mesh_T = (float*)m_T.Array();
    int mesh_T_stride = sizeof(m_T[0])/sizeof(mesh_T[0]);
    if ( Tsd && Tside.Count() != m_V.Count() )
      Tsd = 0;
    AdjustMeshPeriodicTextureCoordinatesHelper( *this, mesh_xform, mesh_T, mesh_T_stride, Tsd ? Tside.Array() : 0, two_pi_tc, mp );
    mesh_T = 0; // when the array is grown, the pointer may become invalid
    if ( !mapping.m_uvw.IsIdentity() && !mapping.m_uvw.IsZero() )
    {
      // Apply the uvw transformation that is on mapping
      // to the texture coordinates.
      ON_2fPoint* meshT = m_T.Array();
      ON_3dPoint T;
      int vi, vcnt = m_T.Count();
      for ( vi = 0; vi < vcnt; vi++ )
      {
        T.x = meshT[vi].x;
        T.y = meshT[vi].y;
        T.z = 0.0;
        T = mapping.m_uvw*T;
        meshT[vi].x = (float)T.x;
        meshT[vi].y = (float)T.y;
      }
    }
  }

  return rc;
}

ON_MappingChannel::ON_MappingChannel()
{
  Default();
}

void ON_MappingChannel::Default()
{
  memset(this,0,sizeof(*this));
  m_mapping_channel_id = 1;
  m_mapping_index = -1;
  m_object_xform = ON_Xform::IdentityTransformation;
}

int ON_MappingChannel::Compare( const ON_MappingChannel& other ) const
{
  int rc = m_mapping_channel_id - other.m_mapping_channel_id;
  if (!rc)
    rc = ON_UuidCompare(m_mapping_id,other.m_mapping_id);
  return rc;
}

bool ON_MappingChannel::Write( ON_BinaryArchive& archive ) const
{
  bool rc = archive.BeginWrite3dmChunk(TCODE_ANONYMOUS_CHUNK,1,1);
  if (rc)
  {
    rc = archive.WriteInt(m_mapping_channel_id);
    if (rc) rc = archive.WriteUuid(m_mapping_id);

    // 1.1 field added 6 June 2006
    if (rc) rc = archive.WriteXform(m_object_xform);

    if ( !archive.EndWrite3dmChunk() )
      rc = false;
  }
  return rc;
}

bool ON_MappingChannel::Read( ON_BinaryArchive& archive )
{
  Default();
  int major_version = 0;
  int minor_version = 0;
  bool rc = archive.BeginRead3dmChunk(TCODE_ANONYMOUS_CHUNK,&major_version,&minor_version);
  if (rc)
  {
    rc = (1 == major_version);
    if (rc) rc = archive.ReadInt(&m_mapping_channel_id);
    if (rc) rc = archive.ReadUuid(m_mapping_id);

    if ( rc && minor_version >= 1 )
    {
      // 1.1 field added 6 June 2006
      if (rc) rc = archive.ReadXform(m_object_xform);
      if (rc 
          && archive.ArchiveOpenNURBSVersion() < 200610030 
          && m_object_xform.IsZero()
          )
      {
        // Between versions 200606060 and 200610030,
        // there was a bug that created some mapping
        // channels with zero transformations.  This
        // if clause finds those and sets them to the
        // identity.
        m_object_xform = ON_Xform::IdentityTransformation;
      }
    }

    if ( !archive.EndRead3dmChunk() )
      rc = false;
  }
  return rc;
}


ON_MaterialRef::ON_MaterialRef()
{
  Default();
}

ON_MappingRef::ON_MappingRef()
{
  Default();
}

void ON_MaterialRef::Default()
{
  memset(this,0,sizeof(*this));
  // runtme index value of -1 means not set
  m_material_index          = -1;
  m_material_backface_index = -1;
  m_material_source = ON::material_from_layer;
}

void ON_MappingRef::Default()
{
  m_plugin_id = ON_nil_uuid;
  m_mapping_channels.Destroy();
}

int ON_MaterialRef::Compare( const ON_MaterialRef& other ) const
{
  int rc = ON_UuidCompare(m_plugin_id,other.m_plugin_id);
  if (rc)
    rc = ((int)m_material_source) - ((int)other.m_material_source);
  if (!rc)
    rc = ON_UuidCompare(m_material_id,other.m_material_id);
  if (!rc)
    rc = ON_UuidCompare(m_material_backface_id,other.m_material_backface_id);
  return rc;
}

int ON_MappingRef::Compare( const ON_MappingRef& other ) const
{
  int rc = ON_UuidCompare(m_plugin_id,other.m_plugin_id);
  if ( !rc)
  {
    const int count = m_mapping_channels.Count();
    rc = count - other.m_mapping_channels.Count();
    if (!rc)
    {
      for ( int i = 0; i < count && !rc; i++ )
      {
        rc = m_mapping_channels[i].Compare(other.m_mapping_channels[i]);
      }
    }
  }
  return rc;
}


bool ON_MaterialRef::Write( ON_BinaryArchive& archive ) const
{
  bool rc = archive.BeginWrite3dmChunk( TCODE_ANONYMOUS_CHUNK, 1, 1 );
  if (rc)
  {
    if (rc) rc = archive.WriteUuid( m_plugin_id );
    if (rc) rc = archive.WriteUuid( m_material_id );

    // 23 May 2006 Dale lear
    //   m_mapping_channels[] was removed from ON_MaterialRef.
    //   To keep from breaking the file format, I need to
    //   write a zero as the array length.
    //
    //if (rc) rc = archive.WriteArray( m_mapping_channels );
    if (rc) rc = archive.WriteInt(0);

    // 23 May 2006 added 
    if (rc) rc = archive.WriteUuid( m_material_backface_id );
    if (rc) rc = archive.WriteInt( m_material_source );


    if ( !archive.EndWrite3dmChunk() )
      rc = false;
  }
  return rc;
}

bool ON_MaterialRef::Read( ON_BinaryArchive& archive )
{
  Default();
  int major_version = 0;
  int minor_version = 0;
  bool rc = archive.BeginRead3dmChunk( TCODE_ANONYMOUS_CHUNK, &major_version, &minor_version );
  if (rc)
  {
    rc = (1 == major_version);

    if (rc) rc = archive.ReadUuid( m_plugin_id );
    if (rc) rc = archive.ReadUuid( m_material_id );

    // 23 May 2006 Dale lear
    //   m_mapping_channels[] was removed from ON_MaterialRef.
    //   To keep from breaking the file format, I need to
    //   write a zero as the array length.
    ON_SimpleArray<ON_MappingChannel> obsolete_mapping_channels;
    if (rc) rc = archive.ReadArray( obsolete_mapping_channels );

    if ( minor_version >= 1 )
    {
      if (rc) rc = archive.ReadUuid( m_material_backface_id );
      int i = m_material_source;
      if (rc) rc = archive.ReadInt( &i );
      if (rc) m_material_source = (unsigned char)ON::ObjectMaterialSource(i);
    }

    if ( !archive.EndRead3dmChunk() )
      rc = false;
  }
  return rc;
}

void ON_MaterialRef::SetMaterialSource(
  ON::object_material_source material_source
  )
{
  m_material_source = (unsigned char)material_source;
}

ON::object_material_source ON_MaterialRef::MaterialSource() const
{
  return ON::ObjectMaterialSource(m_material_source);
}

bool ON_MappingRef::Write( ON_BinaryArchive& archive ) const
{
  bool rc = archive.BeginWrite3dmChunk( TCODE_ANONYMOUS_CHUNK, 1, 0 );
  if (rc)
  {
    if (rc) rc = archive.WriteUuid( m_plugin_id );
    if (rc) rc = archive.WriteArray( m_mapping_channels );
    
    if ( !archive.EndWrite3dmChunk() )
      rc = false;
  }
  return rc;
}

bool ON_MappingRef::Read( ON_BinaryArchive& archive )
{
  Default();
  int major_version = 0;
  int minor_version = 0;
  bool rc = archive.BeginRead3dmChunk( TCODE_ANONYMOUS_CHUNK, &major_version, &minor_version );
  if (rc)
  {
    rc = (1 == major_version);

    if (rc) rc = archive.ReadUuid( m_plugin_id );
    if (rc) rc = archive.ReadArray( m_mapping_channels );

    if ( !archive.EndRead3dmChunk() )
      rc = false;
  }
  return rc;
}

bool ON_MappingRef::Transform( const ON_Xform& xform )
{
  int count = m_mapping_channels.Count();
  if ( count > 0 )
  {
    for ( ON_MappingChannel* mapping_channel = m_mapping_channels.Array();
          count--;
          mapping_channel++ )
    {
      mapping_channel->m_object_xform = xform*mapping_channel->m_object_xform;
    }
  }
  return true;
}

ON_ObjectRenderingAttributes::ON_ObjectRenderingAttributes()
{
  Default();
}

ON_RenderingAttributes::ON_RenderingAttributes()
{
  Default();
}

void ON_ObjectRenderingAttributes::Default()
{
  ON_RenderingAttributes::Default();
  m_mappings.Destroy();
  m_bCastsShadows = true;
  m_bReceivesShadows = true;
  m_bits = 0;
  m_reserved1 = 0;
}

void ON_RenderingAttributes::Default()
{
  m_materials.Destroy();
}

void ON_ObjectRenderingAttributes::EnableAdvancedTexturePreview(bool b)
{
  if ( b )
    m_bits |= 1;    // set bit 1
  else 
    m_bits &= 0xFE; // clear bit 1
}

bool ON_ObjectRenderingAttributes::AdvancedTexturePreview() const
{
  return (0 != (1 & m_bits)) ? true : false;
}

bool ON_RenderingAttributes::IsValid( ON_TextLog* text_log ) const
{
  // plug-in uuids must be unique
  int count;
  if( (count = m_materials.Count()) > 1 )
  {
    const ON_MaterialRef* mr = m_materials.Array();
    ON_UUID plugin_id;
    int i, j;
    for ( i = 0; i < count-1; i++ )
    {
      plugin_id = mr[i].m_plugin_id;
      for ( j = i+1; j < count; j++ )
      {
        if ( !ON_UuidCompare(&plugin_id,&mr[j].m_plugin_id ) )
        {
          if( text_log )
          {
            text_log->Print("ON_RenderingAttributes error: m_materials[%d] and m_materials[%d] have the same plug-in id.\n",i,j);
          }
          return false;
        }
      }
    }    
  }
  return true;
}

bool ON_ObjectRenderingAttributes::IsValid( ON_TextLog* text_log ) const
{
  if ( !ON_RenderingAttributes::IsValid(text_log) )
    return false;

  // plug-in uuids must be unique
  int count;
  if( (count = m_mappings.Count()) > 1 )
  {
    const ON_MappingRef* mr = m_mappings.Array();
    ON_UUID plugin_id;
    int i, j;
    for ( i = 0; i < count-1; i++ )
    {
      plugin_id = mr[i].m_plugin_id;
      for ( j = i+1; j < count; j++ )
      {
        if ( !ON_UuidCompare(&plugin_id,&mr[j].m_plugin_id ) )
        {
          if( text_log )
          {
            text_log->Print("ON_ObjectRenderingAttributes error: m_mappings[%d] and m_mappings[%d] have the same plug-in id.\n",i,j);
          }
          return false;
        }
      }
    }    
  }

  return true;
}

int ON_RenderingAttributes::Compare( const ON_RenderingAttributes& other ) const
{
  const int count = m_materials.Count();
  int rc = count - other.m_materials.Count();
  if (!rc)
  {
    int i;
    for ( i = 0; i < count && !rc; i++ )
    {
      rc = m_materials[i].Compare(other.m_materials[i]);
    }
  }
  return rc;
}

const ON_MaterialRef* ON_RenderingAttributes::MaterialRef( const ON_UUID& plugin_id ) const
{
  int count;
  if ( (count = m_materials.Count()) > 0 )
  {
    for ( const ON_MaterialRef* mr = m_materials.Array(); count--; mr++ )
    {
      if ( plugin_id == mr->m_plugin_id )
        return mr;
    }
  }
  return 0;
}

int ON_ObjectRenderingAttributes::Compare( const ON_ObjectRenderingAttributes& other ) const
{
  int rc = ON_RenderingAttributes::Compare(other);
  if (!rc)
  {
    int i;
    const int count = m_mappings.Count();
    rc = other.m_mappings.Count() - count;
    for ( i = 0; i < count && !rc; i++ )
    {
      rc = m_mappings[i].Compare(other.m_mappings[i]);
    }
    if ( !rc )
    {
      rc = ((int)(m_bCastsShadows?1:0)) - ((int)(other.m_bCastsShadows?1:0));
      if ( !rc )
      {
        rc = ((int)(m_bReceivesShadows?1:0)) - ((int)(other.m_bReceivesShadows?1:0));
      }
	  if ( !rc )
	  {
	    rc = ((int)(AdvancedTexturePreview()?1:0)) - ((int)(other.AdvancedTexturePreview()?1:0));
	  }
    }
  }
  return rc;
}

bool ON_ObjectRenderingAttributes::Transform( const ON_Xform& xform )
{
  int i;
  if ( (i = m_mappings.Count()) > 0 )
  {
    for( ON_MappingRef* mr = m_mappings.Array(); i--; mr++ )
      mr->Transform(xform);
  }
  return true;
}

const ON_MappingRef* ON_ObjectRenderingAttributes::MappingRef(
  const ON_UUID& plugin_id ) const
{
  int count;
  if ( (count = m_mappings.Count()) > 0 )
  {
    for ( const ON_MappingRef* mr = m_mappings.Array(); count--; mr++ )
    {
      if ( plugin_id == mr->m_plugin_id )
        return mr;
    }    
  }

  //ALB 2013.12.03
  //Fixes http://mcneel.myjetbrains.com/youtrack/issue/RH-5730
  //I'm sick of this bug being considered irrelavent, and since I've decided to go out of my way to 
  //Sort out as many mapping problems as I can, I'm fixing this one like this.
  if (m_mappings.Count() > 0)
  {
	  return &m_mappings[0];
  }

  return 0;
}

ON_MappingRef* ON_ObjectRenderingAttributes::AddMappingRef( 
  const ON_UUID& plugin_id 
  )
{
  ON_MappingRef* mr = 0;
  int count;
  if ( (count = m_mappings.Count()) > 0 )
  {
    for ( mr = const_cast<ON_MappingRef*>(m_mappings.Array()); count--; mr++ )
    {
      if ( plugin_id == mr->m_plugin_id )
        break;
    }    
  }

  if ( !mr )
  {
    mr = &m_mappings.AppendNew();
    mr->m_plugin_id = plugin_id;
  }

  return mr;
}

bool ON_ObjectRenderingAttributes::DeleteMappingRef( 
  const ON_UUID& plugin_id 
  )
{
  const ON_MappingRef* mr = MappingRef(plugin_id);
  if ( mr ) 
    m_mappings.Remove( (int)(mr - m_mappings.Array()) ); // safe ptr to in conversion
  return (0 != mr);  
}

const ON_MappingChannel* ON_ObjectRenderingAttributes::MappingChannel( 
  const ON_UUID& plugin_id, 
  const ON_UUID& mapping_id
  ) const
{
  const ON_MappingRef* mr = MappingRef(plugin_id);
  if ( mr )
  {
    int count;
    if ( (count = mr->m_mapping_channels.Count()) > 0 )
    {
      for ( const ON_MappingChannel* mc = mr->m_mapping_channels.Array(); count--; mc++ )
      {
        if ( mapping_id == mc->m_mapping_id )
          return mc;
      }
    }
  }
  return 0;
}

const ON_MappingChannel* ON_ObjectRenderingAttributes::MappingChannel( 
  const ON_UUID& plugin_id, 
  int mapping_channel_id
  ) const
{
  const ON_MappingRef* mr = MappingRef(plugin_id);
  if ( mr )
  {
    int count;
    if ( (count = mr->m_mapping_channels.Count()) > 0 )
    {
      for ( const ON_MappingChannel* mc = mr->m_mapping_channels.Array(); count--; mc++ )
      {
        if ( mapping_channel_id == mc->m_mapping_channel_id )
          return mc;
      }
    }
  }
  return 0;
}



bool ON_ObjectRenderingAttributes::AddMappingChannel(
        const ON_UUID& plugin_id, 
        int mapping_channel_id,
        const ON_UUID& mapping_id
        )
{
  ON_MappingRef* mr = const_cast<ON_MappingRef*>(MappingRef(plugin_id));
  if ( !mr )
  {
    mr = &m_mappings.AppendNew();
    mr->m_plugin_id = plugin_id;
    ON_MappingChannel& mc = mr->m_mapping_channels.AppendNew();
    mc.m_mapping_channel_id = mapping_channel_id;
    mc.m_mapping_id = mapping_id;
    mc.m_mapping_index = -1; // 27th October 2011 John Croudy - constructor is not called by AppendNew().
    mc.m_object_xform = ON_Xform::IdentityTransformation;
    return true;
  }

  return mr->AddMappingChannel(mapping_channel_id,mapping_id);
}

bool ON_ObjectRenderingAttributes::DeleteMappingChannel(
  const ON_UUID& plugin_id, 
  int mapping_channel_id
  )
{
  ON_MappingRef* mr = const_cast<ON_MappingRef*>(MappingRef(plugin_id));
  return mr ? mr->DeleteMappingChannel(mapping_channel_id) : false;
}

bool ON_ObjectRenderingAttributes::DeleteMappingChannel(
  const ON_UUID& plugin_id, 
  const ON_UUID& mapping_id
  )
{
  ON_MappingRef* mr = const_cast<ON_MappingRef*>(MappingRef(plugin_id));
  return mr ? mr->DeleteMappingChannel(mapping_id) : false;
}

bool ON_ObjectRenderingAttributes::ChangeMappingChannel(
  const ON_UUID& plugin_id, 
  int old_mapping_channel_id,
  int new_mapping_channel_id
  )
{
  ON_MappingRef* mr = const_cast<ON_MappingRef*>(MappingRef(plugin_id));
  return mr ? mr->ChangeMappingChannel(old_mapping_channel_id,new_mapping_channel_id) : false;
}

const ON_MappingChannel* ON_MappingRef::MappingChannel( 
  const ON_UUID& mapping_id
  ) const
{
  int count;
  if ( (count = m_mapping_channels.Count()) > 0 )
  {
    for ( const ON_MappingChannel* mc = m_mapping_channels.Array(); count--; mc++ )
    {
      if ( mapping_id == mc->m_mapping_id )
        return mc;
    }
  }
  return 0;
}

const ON_MappingChannel* ON_MappingRef::MappingChannel( 
  int mapping_channel_id
  ) const
{
  int count;
  if ( (count = m_mapping_channels.Count()) > 0 )
  {
    for ( const ON_MappingChannel* mc = m_mapping_channels.Array(); count--; mc++ )
    {
      if ( mapping_channel_id == mc->m_mapping_channel_id )
        return mc;
    }
  }
  return 0;
}



bool ON_MappingRef::AddMappingChannel(
        int mapping_channel_id,
        const ON_UUID& mapping_id
        )
{
  int i;
  if ( (i = m_mapping_channels.Count()) > 0 )
  {
    for ( const ON_MappingChannel* mc = m_mapping_channels.Array(); i--; mc++ )
    {
      if ( mapping_channel_id == mc->m_mapping_channel_id )
      {
        // a matching mapping channel id exists
        // return true if mapping_id matches
        return ( 0 == ON_UuidCompare(&mapping_id,&mc->m_mapping_id) );
      }
    }
  }

  ON_MappingChannel& mc   = m_mapping_channels.AppendNew();
  mc.m_mapping_channel_id = mapping_channel_id;
  mc.m_mapping_id         = mapping_id;
  mc.m_mapping_index      = -1; // 27th October 2011 John Croudy - constructor is not called by AppendNew().
  mc.m_object_xform = ON_Xform::IdentityTransformation;

  return true;
}

bool ON_MappingRef::DeleteMappingChannel(int mapping_channel_id)
{
  const ON_MappingChannel* mc = MappingChannel(mapping_channel_id);
  if ( mc )
  {
    m_mapping_channels.Remove((int)(mc - m_mapping_channels.Array()));
  }
  return ( 0 != mc);
}

bool ON_MappingRef::DeleteMappingChannel(const ON_UUID& mapping_id)
{
  const ON_MappingChannel* mc = MappingChannel(mapping_id);
  if ( mc )
  {
    m_mapping_channels.Remove((int)(mc - m_mapping_channels.Array()));
  }
  return ( 0 != mc);
}

bool ON_MappingRef::ChangeMappingChannel(
  int old_mapping_channel_id,
  int new_mapping_channel_id
  )
{
  ON_MappingChannel* mc = const_cast<ON_MappingChannel*>(MappingChannel(old_mapping_channel_id));
  if ( mc )
  {
    mc->m_mapping_channel_id = new_mapping_channel_id;
  }
  return ( 0 != mc );
}

bool ON_RenderingAttributes::Write( ON_BinaryArchive& archive ) const
{
  bool rc = archive.BeginWrite3dmChunk( TCODE_ANONYMOUS_CHUNK, 1, 0 );
  if ( !rc )
    return false;
  for(;;)
  {
    rc = archive.WriteArray(m_materials);
    if ( !rc ) break;

    break;
  }
  if ( !archive.EndWrite3dmChunk() )
    rc = false;
  return rc;
}

bool ON_RenderingAttributes::Read( ON_BinaryArchive& archive )
{
  Default();
  int major_version = 0;
  int minor_version = 0;
  bool rc = archive.BeginRead3dmChunk( TCODE_ANONYMOUS_CHUNK, &major_version, &minor_version );
  if (!rc) 
    return false;
  for(;;)
  {
    rc = ( 1 == major_version );
    if (!rc) break;
    rc = archive.ReadArray(m_materials);
    if (!rc) break;

    break;
  }
  if ( !archive.EndRead3dmChunk() )
    rc = false;
  return rc;
}

bool ON_ObjectRenderingAttributes::Write( ON_BinaryArchive& archive ) const
{
  bool rc = archive.BeginWrite3dmChunk( TCODE_ANONYMOUS_CHUNK, 1, 3 );
  if ( !rc )
    return false;
  for(;;)
  {
    // DO NOT CALL ON_RenderingAttributes::Write 
    rc = archive.WriteArray(m_materials);
    if ( !rc ) break;
    rc = archive.WriteArray(m_mappings);
    if ( !rc ) break;

    // version 1.2 fields added 20061129
    rc = archive.WriteBool(m_bCastsShadows);
    if ( !rc ) break;
    rc = archive.WriteBool(m_bReceivesShadows);
    if ( !rc ) break;

    // version 1.3 fields added 20101019
    bool b = AdvancedTexturePreview();
    rc = archive.WriteBool(b);
    if ( !rc ) break;

    break;
  }
  if ( !archive.EndWrite3dmChunk() )
    rc = false;
  return rc;
}

bool ON_ObjectRenderingAttributes::Read( ON_BinaryArchive& archive )
{
  Default();
  int major_version = 0;
  int minor_version = 0;
  bool rc = archive.BeginRead3dmChunk( TCODE_ANONYMOUS_CHUNK, &major_version, &minor_version );
  if (!rc) 
    return false;
  for(;;)
  {
    rc = ( 1 == major_version && minor_version >= 1 );
    if (!rc) break;

    // DO NOT CALL ON_RenderingAttributes::Read 
    if (rc) rc = archive.ReadArray(m_materials);
    if (!rc) break;
    if (rc) rc = archive.ReadArray(m_mappings);
    if (!rc) break;

    if ( minor_version <= 1 )
      break;

    // version 1.2 fields added 20061129
    rc = archive.ReadBool(&m_bCastsShadows);
    if ( !rc ) break;
    rc = archive.ReadBool(&m_bReceivesShadows);
    if ( !rc ) break;

    if ( minor_version <= 2 )
      break;

    // version 1.3 fields added 20101019
    bool b = AdvancedTexturePreview();
    rc = archive.ReadBool(&b);
    if ( !rc ) break;
    // Jussi 20120430: We don't want to enable advanced texture preview by default. It will be
    //                 turned on when needed (depending on active render plug-in etc).
    //EnableAdvancedTexturePreview(b);

    break;
  }
  if ( !archive.EndRead3dmChunk() )
    rc = false;

  return rc;
}


bool ON_TextureMapping::SetSurfaceParameterMapping(void)
{
  // The nullptr check is wierd.
  // Speculation: A reference was null and somebody added this
  // as a hack to prevent a crash.
  if ( false == ON_IsNullPtr(this) )
  {
    *this = ON_TextureMapping::SurfaceParameterTextureMapping;
    SetId(); // new id
  }
	return true;
}


bool ON_TextureMapping::SetPlaneMapping(
          const ON_Plane& plane,
          const ON_Interval& dx,
          const ON_Interval& dy,
          const ON_Interval& dz
          )
{
  *this = ON_TextureMapping::Unset;

  // Don't call plane.IsValid(), because the plane
  // equation does not matter and many developers
  // forget to set it correctly.
  if ( !plane.origin.IsValid() )
    return false;
  if ( !ON_IsRightHandFrame( plane.xaxis, plane.yaxis, plane.zaxis ) )
    return false;
  if ( !dx.IsValid() || !dy.IsValid() || !dz.IsValid() )
    return false;

  ON_3dPoint C = plane.PointAt(dx.Mid(),dy.Mid(),dz.Mid());
  C.x = (0.0 == C.x) ? 0.0 : -C.x;
  C.y = (0.0 == C.y) ? 0.0 : -C.y;
  C.z = (0.0 == C.z) ? 0.0 : -C.z;
  ON_3dVector xaxis = plane.xaxis;
  ON_3dVector yaxis = plane.yaxis;
  ON_3dVector zaxis = plane.zaxis;

  // Any "cleanup" needs to be done here 
  // to xaxis, yaxis, zaxis.
  
  double sx,sy,sz;
  if ( 0.0 == (sx = dx.Length())) sx = 2.0;
  if ( 0.0 == (sy = dy.Length())) sy = 2.0;
  if ( 0.0 == (sz = dz.Length())) sz = 2.0;

  // The plane mapping matrix m_Pxyz transforms the
  // world coordinate rectangle to a (-1<=r<=1,
  // on plane to a 
  // 1 X 1 square in the xy plane centered at the
  // origin.  

  // m_Pxyz = surface point transformation
  ON_3dVector X = (2.0/sx)*xaxis;
  ON_3dVector Y = (2.0/sy)*yaxis;
  ON_3dVector Z = (2.0/sz)*zaxis;

  m_Pxyz.m_xform[0][0] = X.x;
  m_Pxyz.m_xform[0][1] = X.y;
  m_Pxyz.m_xform[0][2] = X.z;
  m_Pxyz.m_xform[0][3] = (X.x*C.x + X.y*C.y + X.z*C.z);

  m_Pxyz.m_xform[1][0] = Y.x;
  m_Pxyz.m_xform[1][1] = Y.y;
  m_Pxyz.m_xform[1][2] = Y.z;
  m_Pxyz.m_xform[1][3] = (Y.x*C.x + Y.y*C.y + Y.z*C.z);

  m_Pxyz.m_xform[2][0] = Z.x;
  m_Pxyz.m_xform[2][1] = Z.y;
  m_Pxyz.m_xform[2][2] = Z.z;
  m_Pxyz.m_xform[2][3] = (Z.x*C.x + Z.y*C.y + Z.z*C.z);

  m_Pxyz.m_xform[3][0] = 0.0;
  m_Pxyz.m_xform[3][1] = 0.0;
  m_Pxyz.m_xform[3][2] = 0.0;
  m_Pxyz.m_xform[3][3] = 1.0;

  // m_Nxyz = surface normal transformation
  //        = inverse transpose of upper 3x3 of m_Pxyz
  X = (0.5*sx)*xaxis;
  Y = (0.5*sy)*yaxis;
  Z = (0.5*sz)*zaxis;
  m_Nxyz.m_xform[0][0] = X.x;
  m_Nxyz.m_xform[0][1] = X.y;
  m_Nxyz.m_xform[0][2] = X.z;
  m_Nxyz.m_xform[0][3] = 0.0;

  m_Nxyz.m_xform[1][0] = Y.x;
  m_Nxyz.m_xform[1][1] = Y.y;
  m_Nxyz.m_xform[1][2] = Y.z;
  m_Nxyz.m_xform[1][3] = 0.0;

  m_Nxyz.m_xform[2][0] = Z.x;
  m_Nxyz.m_xform[2][1] = Z.y;
  m_Nxyz.m_xform[2][2] = Z.z;
  m_Nxyz.m_xform[2][3] = 0.0;

  m_Nxyz.m_xform[3][0] = 0.0;
  m_Nxyz.m_xform[3][1] = 0.0;
  m_Nxyz.m_xform[3][2] = 0.0;
  m_Nxyz.m_xform[3][3] = 1.0;

  m_type = ON_TextureMapping::TYPE::plane_mapping;
  SetId();

#if defined(ON_DEBUG)
  {
    ON_Plane p;
    p.xaxis = (2.0/sx)*plane.xaxis;
    p.yaxis = (2.0/sy)*plane.yaxis;
    p.zaxis = (2.0/sz)*plane.zaxis;
    p.origin.Set(-C.x,-C.y,-C.z);
    p.UpdateEquation();
    ON_Xform P_dbg, N_dbg;
    P_dbg.Rotation(p,ON_xy_plane);
    P_dbg.GetSurfaceNormalXform(N_dbg);

    for ( int i = 0; i < 4; i++ )
    {
      for ( int j = 0; j < 4; j++ )
      {
        if ( fabs(m_Pxyz[i][j] - P_dbg[i][j]) >= ON_SQRT_EPSILON*(fabs(m_Pxyz[i][j])+128.0) )
        {
          ON_ERROR("m_Pxyz is nor right\n");
          break;
        }
        if ( fabs(m_Nxyz[i][j] - N_dbg[i][j]) >= ON_SQRT_EPSILON*(fabs(m_Nxyz[i][j])+128.0) )
        {
          ON_ERROR("m_Nxyz is nor right\n");
          break;
        }
      }
    }
  }
#endif
	return true;
}

bool ON_TextureMapping::SetBoxMapping(const ON_Plane& plane,
                                      ON_Interval dx,
                                      ON_Interval dy,
                                      ON_Interval dz,
                                      bool bCapped 
                                      )
{
  bool rc = SetPlaneMapping(plane,dx,dy,dz);
  if (rc)
  {
    m_bCapped = bCapped;
    m_type = ON_TextureMapping::TYPE::box_mapping;
  }
  return rc;
}

bool ON_TextureMapping::SetCylinderMapping(const ON_Cylinder& cylinder, bool bIsCapped)
{
  ON_Interval dr, dh;
  if ( !ON_IsValid(cylinder.circle.radius ) )
    return false;
  double r = cylinder.circle.radius;
  if ( 0.0 == r )
    r = 1.0;
  dr.Set(-r,r);
  dh.Set(cylinder.height[0],cylinder.height[1]);
  if ( dh[0] == dh[1] )
  {
    if ( ON_UNSET_VALUE == dh[0] )
    {
      dh.Set(-1.0,1.0);
    }
    else
    {
      dh.m_t[0] -= 1.0;
      dh.m_t[0] += 1.0;
    }
  }
  if ( !dh.IsValid() )
    return false;

  bool rc = SetBoxMapping(cylinder.circle.plane,dr,dr,dh,bIsCapped);
  if (rc)
  {
	  m_type = ON_TextureMapping::TYPE::cylinder_mapping;
  }

	return rc;
}

bool ON_TextureMapping::SetSphereMapping(const ON_Sphere& sphere)
{
  ON_Interval dr(-sphere.radius,sphere.radius);
  bool rc = SetBoxMapping(sphere.plane,dr,dr,dr,false);
  if (rc)
  {
	  m_type = ON_TextureMapping::TYPE::sphere_mapping;
  }
	return rc;
}



bool ON_TextureMapping::GetMappingPlane(ON_Plane& plane,
                                        ON_Interval& dx,
                                        ON_Interval& dy,
                                        ON_Interval& dz
                                        ) const
{
  ON_Xform xform(m_Pxyz);

  ON_3dVector S(((ON_3dVector*)&xform.m_xform[0])->Length(),
                ((ON_3dVector*)&xform.m_xform[1])->Length(),
                ((ON_3dVector*)&xform.m_xform[2])->Length());

  if ( 0.0 == S.x )
    return false;
  S.x = 1.0/S.x;
  if ( 0.0 == S.y )
    return false;
  S.y = 1.0/S.y;
  if ( 0.0 == S.z )
    return false;
  S.z = 1.0/S.z;

  xform.m_xform[0][0] *= S.x; xform.m_xform[0][1] *= S.x; xform.m_xform[0][2] *= S.x;
  xform.m_xform[0][3] *= S.x;  
  
  xform.m_xform[1][0] *= S.y; xform.m_xform[1][1] *= S.y; xform.m_xform[1][2] *= S.y;
  xform.m_xform[1][3] *= S.y;  

  xform.m_xform[2][0] *= S.z; xform.m_xform[2][1] *= S.z; xform.m_xform[2][2] *= S.z;
  xform.m_xform[2][3] *= S.z;

  xform.m_xform[3][0] = 0.0;
  xform.m_xform[3][1] = 0.0;
  xform.m_xform[3][2] = 0.0;
  xform.m_xform[3][3] = 1.0;

  ON_Xform inv(xform);
  if ( !inv.Invert() )
    return false;

  plane.origin.Set(inv.m_xform[0][3],inv.m_xform[1][3],inv.m_xform[2][3]);
  xform.m_xform[0][3] = 0.0; 
  xform.m_xform[1][3] = 0.0;
  xform.m_xform[2][3] = 0.0;
  plane.xaxis = &xform.m_xform[0][0];
  plane.yaxis = &xform.m_xform[1][0];
  plane.zaxis = &xform.m_xform[2][0];

	plane.UpdateEquation();

  dx.Set(-S.x,S.x);
  dy.Set(-S.y,S.y);
  dz.Set(-S.z,S.z);

  return plane.IsValid();
}

bool ON_TextureMapping::GetMappingBox(ON_Plane& plane,
                                      ON_Interval& dx,
                                      ON_Interval& dy,
                                      ON_Interval& dz) const
{
	return GetMappingPlane(plane, dx, dy, dz);
}

bool ON_TextureMapping::GetMappingCylinder(ON_Cylinder& cylinder) const
{
  ON_Interval dx, dy, dz;
  ON_Plane plane;
  bool rc = GetMappingPlane(cylinder.circle.plane, dx, dy, dz);
  if (rc)
  {
    double r0 = 0.5*dx.Length();
    double r1 = 0.5*dy.Length();
    cylinder.circle.radius = (r0 == r1) ? r0 : 0.5*(r0+r1);
    cylinder.height[0] = dz[0];
    cylinder.height[1] = dz[1];
  }

  return rc && cylinder.IsValid();
}

bool ON_TextureMapping::GetMappingSphere(ON_Sphere& sphere) const
{
  ON_Interval dx, dy, dz;
  bool rc = GetMappingPlane(sphere.plane, dx, dy, dz);
  if (rc)
  {
    double r0 = 0.5*dx.Length();
    double r1 = 0.5*dy.Length();
    double r2 = 0.5*dz.Length();
    sphere.radius = (r0 == r1 && r0 == r2) ? r0 : (r0+r1+r2)/3.0;
  }
  return rc && sphere.IsValid();
}

