with import <nixpkgs> {};

python3Packages.buildPythonPackage rec {
    name = "djroomba-0.1";
    src = fetchurl {
        url = "https://github.com/acm-uiuc/DJ-Roomba/archive/master.zip";
        sha256 = "638bbb47ca7a436d8eecd345e5efe5ff0f121276aab91f735bfb686b77e59bc3";
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
