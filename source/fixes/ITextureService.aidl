package io.github.astromg01.massaff.service;

interface ITextureService {
    void destroy() = 16777114; // Reserved transaction used by the Shizuku server.
    void exit() = 1;
    String ping() = 2;
    String inspectAngle(String gamePackage) = 3;
    String captureState(String gamePackage) = 4;
    String applyClayProfile(String gamePackage, int lodOffset, String snapshotJson) = 5;
    String restoreState(String snapshotJson) = 6;
    String readAngleLogs(String gamePackage, int lodOffset) = 7;
}
