## the first way

>cd celeritas
> go mod init github.com/iadaria/celeritas

>cd ../myapp

>open go.mod

>add replace github.com/iadaria/celeritas => ../celeritas

> go get github.com/iadaria/celeritas

>go run .

After update celeritas lib: > go get -u github.com/iadaria/celeritas

## the second way
add new functon to package
> cd myapp
> go mod vendor
- Visual code: >reload windows(not always)

## the third way - use the make https://www.gnu.org/software/make/
> create Makefile in root folder
Shift + tab - delete tab
Macos + alt - multiple cursor
Should be one single 
> make run