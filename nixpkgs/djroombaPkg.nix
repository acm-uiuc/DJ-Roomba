with import <nixpkgs> {};

python3Packages.buildPythonPackage rec {
    name = "djroomba-0.1";
    src = fetchurl {
        url = "https://github.com/acm-uiuc/DJ-Roomba/archive/master.tar.gz";
        sha256 = "1f0aa06d0eaceeb7474278e3dadbcc18a731803f4d2da377822a88bdabfebe57";
    };

    propagatedBuildInputs = with python3Packages; [
         pyusb
         click
         pyserial
         (import ./evdev.nix)
         (import ./amqp.nix)
         (import ./gpio.nix)
         (import ./pyroomba.nix)
    ];
    
    doCheck = false;
}
