#include <Eigen/Core>

using namespace Eigen;

inline MatrixXi& c_to_eigen(C_MatrixXi* ptr)
{
                return *reinterpret_cast<MatrixXi*>(ptr);
}
inline C_MatrixXi* eigen_to_c(MatrixXi& ref)
{
                return reinterpret_cast<C_MatrixXi*>(&ref);
}

inline Map<MatrixXi>& c_to_eigen(C_Map_MatrixXi* ptr)
{
                return *reinterpret_cast<Map<MatrixXi>*>(ptr);
}

inline const Map<MatrixXi>& c_to_eigen(const C_Map_MatrixXi* ptr)
{
                return *reinterpret_cast<const Map<MatrixXi>*>(ptr);
}

inline C_Map_MatrixXi* eigen_to_c(Map<MatrixXi>& ref)
{
                return reinterpret_cast<C_Map_MatrixXi*>(&ref);
}

inline const C_Map_MatrixXi* eigen_to_c(const Map<MatrixXi>& ref)
{
                return reinterpret_cast<const C_Map_MatrixXi*>(&ref);
}

