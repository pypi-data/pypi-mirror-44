#include "bindings.h"

#pragma once

#if defined(ON_PYTHON_COMPILE)
void initSurfaceBindings(pybind11::module& m);
#else
void initSurfaceBindings(void* m);
#endif

class BND_Surface : public BND_GeometryBase
{
public:
  ON_Surface* m_surface = nullptr;
protected:
  BND_Surface();
  void SetTrackedPointer(ON_Surface* surface, const ON_ModelComponentReference* compref);

public:
  BND_Surface(ON_Surface* surface, const ON_ModelComponentReference* compref);
  bool IsSolid() const { return m_surface->IsSolid(); }
  //public Interval Domain(int direction)
  //public virtual bool SetDomain(int direction, Interval domain)
  int Degree(int direction) const { return m_surface->Degree(direction); }
  int SpanCount(int direction) const { return m_surface->SpanCount(direction); }
  //public double[] GetSpanVector(int direction)
  //public Surface Reverse(int direction)
  //public Surface Reverse(int direction, bool inPlace)
  //public Surface Transpose()
  //public Surface Transpose(bool inPlace)
  ON_3dPoint PointAt(double u, double v) const { return m_surface->PointAt(u, v); }
  ON_3dVector NormalAt(double u, double v) const { return m_surface->NormalAt(u, v); }
  //public bool FrameAt(double u, double v, out Plane frame)
  //public SurfaceCurvature CurvatureAt(double u, double v)
  //public IsoStatus IsIsoparametric(Curve curve, Interval curveDomain)
  //public IsoStatus IsIsoparametric(Curve curve)
  //public IsoStatus IsIsoparametric(BoundingBox bbox)
  bool IsClosed(int direction) const { return m_surface->IsClosed(direction); }
  bool IsPeriodic(int direction) const { return m_surface->IsPeriodic(direction); }
  bool IsSingular(int side) const { return m_surface->IsSingular(side); }
  bool IsAtSingularity(double u, double v, bool exact) const { return m_surface->IsAtSingularity(u, v, exact); }
  int IsAtSeam(double u, double v) const { return m_surface->IsAtSeam(u, v); }
  //public bool IsContinuous(Continuity continuityType, double u, double v)
  //public bool GetNextDiscontinuity(int direction, Continuity continuityType, double t0, double t1, out double t)
  //public Surface Trim(Interval u, Interval v)
  //public bool Evaluate(double u, double v, int numberDerivatives, out Point3d point, out Vector3d[] derivatives)
  //public Curve IsoCurve(int direction, double constantParameter)
  //public Surface[] Split(int direction, double parameter)
  //public Brep ToBrep()
  //public int HasNurbsForm()
  //public NurbsSurface ToNurbsSurface()
  //public NurbsSurface ToNurbsSurface(double tolerance, out int accuracy)
  bool IsPlanar(double tolerance = ON_ZERO_TOLERANCE) const { return m_surface->IsPlanar(nullptr, tolerance); }
  //public bool TryGetPlane(out Plane plane)
  //public bool TryGetPlane(out Plane plane, double tolerance)
  bool IsSphere(double tolerance = ON_ZERO_TOLERANCE) const { return m_surface->IsSphere(nullptr, tolerance); }
  //public bool TryGetSphere(out Sphere sphere)
  //public bool TryGetSphere(out Sphere sphere, double tolerance)
  bool IsCylinder(double tolerance = ON_ZERO_TOLERANCE) const { return m_surface->IsCylinder(nullptr, tolerance); }
  //public bool TryGetCylinder(out Cylinder cylinder)
  //public bool TryGetCylinder(out Cylinder cylinder, double tolerance)
  //public bool TryGetFiniteCylinder(out Cylinder cylinder, double tolerance)
  bool IsCone(double tolerance = ON_ZERO_TOLERANCE) const { return m_surface->IsCone(nullptr, tolerance); }
  //public bool TryGetCone(out Cone cone)
  //public bool TryGetCone(out Cone cone, double tolerance)
  bool IsTorus(double tolerance = ON_ZERO_TOLERANCE) const { return m_surface->IsTorus(nullptr, tolerance); }
  //public bool TryGetTorus(out Torus torus)
  //public bool TryGetTorus(out Torus torus, double tolerance)
  //public bool GetSurfaceParameterFromNurbsFormParameter(double nurbsS, double nurbsT, out double surfaceS, out double surfaceT)
  //public bool GetNurbsFormParameterFromSurfaceParameter(double surfaceS, double surfaceT, out double nurbsS, out double nurbsT)
};
