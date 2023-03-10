### Update project

>go mod init github.com/iadaria/myapp

>go clean -modcache

> go get github.com/iadaria/celeritas
> go get -u github.com/iadaria/celeritas
> go mod vendor

module myapp

go 1.19

replace github.com/iadaria/celeritas => ../celeritas

require github.com/iadaria/celeritas v0.0.0-00010101000000-000000000000