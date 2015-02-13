with import <nixpkgs> {};

python3Packages.buildPythonPackage rec {
    name = "pyroomba-0.1.0";
    src = fetchurl {
        url = "https://github.com/mvcisback/pyroomba/archive/master.zip";
        sha256 = "a9fc154879cb4dcfca46ee2297ad2f99b1ab5c47e5b3d9500383a837935dcbe6";
    };

    propagatedBuildInputs = with python3Packages; [
        pyserial
    ];

    
    doCheck = false;
}
