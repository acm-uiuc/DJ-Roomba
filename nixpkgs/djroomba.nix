let
    pkgs = import <nixpkgs> {};
    stdenv = pkgs.stdenv;
 in rec {
     djroombaEnv = stdenv.mkDerivation rec {
       name = "djroomba-env";
       buildInputs = with pkgs; [
            git
            python34Packages.pyusb
            python34Packages.click
            python34Packages.pyserial
            python34Packages.virtualenv
            python34
            python27
            python27Packages.virtualenv
            python27Packages.click
            stdenv
            linuxHeaders
            pulseaudio
            (import ./evdev.nix)
            (import ./amqp.nix)
            (import ./gpio.nix)
            (import ./pyroomba.nix)
            (import ./audioLazy.nix)
            wget
            emacs
            python34Packages.ipython
            mpd
       ];
       C_INCLUDE_PATH="${pkgs.linuxHeaders}";
     };

}
