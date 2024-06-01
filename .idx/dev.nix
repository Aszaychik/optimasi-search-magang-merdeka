

# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-23.11"; # or "unstable"
  # Use https://search.nixos.org/packages to find packages
  packages = [ pkgs.python3 pkgs.gnumake42];
  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    workspace = {
      # Runs when a workspace is first created with this `dev.nix` file
      onStart = {
        install =
          "python -m venv .venv         && source .venv/bin/activate         && make run";
      };
      # To run something each time the workspace is (re)started, use the `onStart` hook
    };
    # Enable previews and customize configuration
    previews = {
      enable = false;
      previews = {
        web = {
          command = [ "make run" ];
          env = { PORT = "$PORT"; };
          manager = "web";
        };
      };
    };
  };
}
