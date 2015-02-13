with import <nixpkgs> {};

pythonPackages.buildPythonPackage rec {
    name = "amqp-1.4.6";
    src = fetchurl {
        url = "https://github.com/celery/py-amqp/archive/v1.4.6.tar.gz";
        sha256 = "c4199723844ed9ca9af38019cb5938d096382346b5372f18705d6dcc55c6103f";
    };
    
    doCheck = false;
}
