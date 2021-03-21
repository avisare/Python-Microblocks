namespace sm_data {
enum NavCov_Status
{
    NAV_COV_STS_NO_DATA = 0,  /*  No valid data in covData */
    NAV_COV_STS_DIAGONAL_ONLY = 1,  /*  covData(0,0) = azimuthCov;
                                        covData(1,1) = pitchCov;
                                        covData(2,2) = rollCov;
                                        covData(3,3) = latitudeCov;
                                        covData(4,4) = longitudeCov;
                                        covData(5,5) = altitudeCov;

                                        all other cells are 0. */
    NAV_COV_STS_FULL_MATRIX = 2   /*  covData matrix is full */
};

struct NavCov_Record
{
    NavCov_Status           covStatus;
    float                   floatVar;
};
struct test
{
    int                     testArr[10][10];
    int                     regularArr[10];
};
}