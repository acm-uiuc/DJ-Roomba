with import <nixpkgs> {};

python3Packages.buildPythonPackage rec {
    name = "rpigpio-0.5.10";
    src = fetchurl {
        url = "https://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.5.10.tar.gz";
        sha256 = "bfbcd452ec8caad932fba433e897d3b9361f567a32e39cfad52e5948f6a397c0";
    };

    doCheck = false;
}
