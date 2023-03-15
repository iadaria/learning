- install make
Macos
> brew install make

Windows:
> choco install make

### init
> go mod init github.com/iadaria/celeritas


module myapp

go 1.19

replace github.com/iadaria/celeritas => ../celeritas

require github.com/iadaria/celeritas v0.0.0-00010101000000-000000000000 // indirect