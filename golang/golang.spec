%define repo https://github.com/golang/go.git
%define git_version %(echo `curl -s https://github.com/golang/go/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">ob2' | sed -e 's/r/.0/g'`)
%global _binaries_in_noarch_packages_terminate_build 0
%global __requires_exclude_from ^(%{_datadir}|/usr/lib)/%{name}/(doc|src)/.*$
%define _use_internal_dependency_generator 0
%define __find_requires %{nil}
%global __spec_install_post /usr/lib/rpm/check-rpaths   /usr/lib/rpm/check-buildroot  /usr/lib/rpm/brp-compress
%define release_ver 10
%global revision %(echo `git ls-remote %{repo}  | head -1 | cut -f 1 | cut -c1-7`)

Name:           golang
#Version:        %{git_version}
Version:        1.10
Release:        %{release_ver}.%{revision}.%{dist}
Summary:        The Go Programming Language
License:        BSD
URL:            http://golang.org/
BuildRequires:  golang > 1.4 git pcre-devel /bin/hostname 
BuildRequires:  golang-rpm-macros
#Provides:       go = %{version}-%{release}
Provides:       %{name} = %{version}-%{release}
Requires:       %{name}-bin
Requires:       %{name}-src = %{version}-%{release}
Obsoletes:      %{name}-docs < 1.1-4
Obsoletes:      %{name}-data < 1.1.1-4
Obsoletes:      %{name}-vim < 1.4
Obsoletes:      emacs-%{name} < 1.4
Source100:      golang-gdbinit
Source101:      golang-prelink.conf

%description
%{summary}.

%package       docs
Summary:       Golang compiler docs
Requires:      %{name} = %{version}-%{release}
BuildArch:     noarch
Obsoletes:     %{name}-docs < 1.1-4

%description   docs
%{summary}.

%package       misc
Summary:       Golang compiler miscellaneous sources
Requires:      %{name} = %{version}-%{release}
BuildArch:     noarch

%description   misc
%{summary}.

%package       tests
Summary:       Golang compiler tests for stdlib
Requires:      %{name} = %{version}-%{release}
BuildArch:     noarch

%description   tests
%{summary}.

%package       src
Summary:       Golang compiler source tree
BuildArch:     noarch
Requires:     %{name} = %{version}-%{release}
%description   src
%{summary}

%package        bin
Summary:        Golang core compiler tools
Requires:       %{name} = %{version}-%{release}
Obsoletes:      %{name}-pkg-bin-linux-386 < 1.4.99
Obsoletes:      %{name}-pkg-bin-linux-amd64 < 1.4.99
Obsoletes:      %{name}-pkg-bin-linux-arm < 1.4.99
Obsoletes:      %{name}-pkg-linux-386 < 1.4.99
Obsoletes:      %{name}-pkg-linux-amd64 < 1.4.99
Obsoletes:      %{name}-pkg-linux-arm < 1.4.99
Obsoletes:      %{name}-pkg-darwin-386 < 1.4.99
Obsoletes:      %{name}-pkg-darwin-amd64 < 1.4.99
Obsoletes:      %{name}-pkg-windows-386 < 1.4.99
Obsoletes:      %{name}-pkg-windows-amd64 < 1.4.99
Obsoletes:      %{name}-pkg-plan9-386 < 1.4.99
Obsoletes:      %{name}-pkg-plan9-amd64 < 1.4.99
Obsoletes:      %{name}-pkg-freebsd-386 < 1.4.99
Obsoletes:      %{name}-pkg-freebsd-amd64 < 1.4.99
Obsoletes:      %{name}-pkg-freebsd-arm < 1.4.99
Obsoletes:      %{name}-pkg-netbsd-386 < 1.4.99
Obsoletes:      %{name}-pkg-netbsd-amd64 < 1.4.99
Obsoletes:      %{name}-pkg-netbsd-arm < 1.4.99
Obsoletes:      %{name}-pkg-openbsd-386 < 1.4.99
Obsoletes:      %{name}-pkg-openbsd-amd64 < 1.4.99
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Requires:       glibc
Requires:       gcc

%description    bin
%{summary}

%pretrans -p <lua>
for _,d in pairs({"api", "doc", "include", "lib", "src"}) do
  path = "%{goroot}/" .. d
  if posix.stat(path, "type") == "link" then
    os.remove(path)
    posix.mkdir(path)
  end
end

%package        shared
Summary:        Golang shared object libraries

%description    shared
%{summary}.

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%build
cd %{name}-%{version}
export GOROOT_BOOTSTRAP=%{goroot}
export GOROOT=%{goroot}
export GOPATH=%{gopath}
export GOROOT_FINAL=%{goroot}
export GOHOSTOS=linux
export GOHOSTARCH=%{gohostarch}

#if [ ! -f %{buildroot}%{goroot}/bin/go ]; then
#%__ln_s %{goroot}/bin/linux_amd64/go %{buildroot}%{goroot}/bin/go
#fi
pushd src
CFLAGS="$RPM_OPT_FLAGS" \
LDFLAGS="$RPM_LD_FLAGS" \
CC="gcc" \
CC_FOR_TARGET="gcc" \
GOOS=linux \
GOARCH=%{gohostarch} \
    ./make.bash --no-clean
popd
GOROOT=$(pwd) PATH=$(pwd)/bin:$PATH go install -buildmode=shared std

%install
cd %{name}-%{version}
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{goroot}
cp -apv api bin doc favicon.ico lib pkg robots.txt src misc test VERSION.cache AUTHORS CONTRIBUTORS PATENTS LICENSE $RPM_BUILD_ROOT%{goroot}
#cp -apv api bin doc favicon.ico lib pkg robots.txt src misc test VERSION AUTHORS CONTRIBUTORS PATENTS LICENSE $RPM_BUILD_ROOT%{goroot}
touch $RPM_BUILD_ROOT%{goroot}/pkg
find $RPM_BUILD_ROOT%{goroot}/pkg -exec touch -r $RPM_BUILD_ROOT%{goroot}/pkg "{}" \;
cwd=$(pwd)
src_list=$cwd/go-src.list
pkg_list=$cwd/go-pkg.list
shared_list=$cwd/go-shared.list
misc_list=$cwd/go-misc.list
docs_list=$cwd/go-docs.list
tests_list=$cwd/go-tests.list
rm -f $src_list $pkg_list $docs_list $misc_list $tests_list $shared_list
touch $src_list $pkg_list $docs_list $misc_list $tests_list $shared_list
pushd $RPM_BUILD_ROOT%{goroot}
    find src/ -type d -a \( ! -name testdata -a ! -ipath '*/testdata/*' \) -printf '%%%dir %{goroot}/%p\n' >> $src_list
    find src/ ! -type d -a \( ! -ipath '*/testdata/*' -a ! -name '*_test*.go' \) -printf '%{goroot}/%p\n' >> $src_list
    find bin/ pkg/ -type d -a ! -path '*_dynlink/*' -printf '%%%dir %{goroot}/%p\n' >> $pkg_list
    find bin/ pkg/ ! -type d -a ! -path '*_dynlink/*' -printf '%{goroot}/%p\n' >> $pkg_list
    find doc/ -type d -printf '%%%dir %{goroot}/%p\n' >> $docs_list
    find doc/ ! -type d -printf '%{goroot}/%p\n' >> $docs_list
    find misc/ -type d -printf '%%%dir %{goroot}/%p\n' >> $misc_list
    find misc/ ! -type d -printf '%{goroot}/%p\n' >> $misc_list
    find pkg/*_dynlink/ -type d -printf '%%%dir %{goroot}/%p\n' >> $shared_list
    find pkg/*_dynlink/ ! -type d -printf '%{goroot}/%p\n' >> $shared_list
    find test/ -type d -printf '%%%dir %{goroot}/%p\n' >> $tests_list
    find test/ ! -type d -printf '%{goroot}/%p\n' >> $tests_list
    find src/ -type d -a \( -name testdata -o -ipath '*/testdata/*' \) -printf '%%%dir %{goroot}/%p\n' >> $tests_list
    find src/ ! -type d -a \( -ipath '*/testdata/*' -o -name '*_test*.go' \) -printf '%{goroot}/%p\n' >> $tests_list
    find lib/ -type d -printf '%%%dir %{goroot}/%p\n' >> $tests_list
    find lib/ ! -type d -printf '%{goroot}/%p\n' >> $tests_list
popd
rm -rfv $RPM_BUILD_ROOT%{goroot}/doc/Makefile
%{__mkdir_p} %{buildroot}%{goroot}/bin/linux_%{gohostarch}
ln -sf %{goroot}/bin/go $RPM_BUILD_ROOT%{goroot}/bin/linux_%{gohostarch}/go
ln -sf %{goroot}/bin/gofmt $RPM_BUILD_ROOT%{goroot}/bin/linux_%{gohostarch}/gofmt
%{__mkdir_p} %{buildroot}%{gopath}/src/github.com
%{__mkdir_p} %{buildroot}%{gopath}/src/bitbucket.org
%{__mkdir_p} %{buildroot}%{gopath}/src/code.google.com
%{__mkdir_p} %{buildroot}%{gopath}/src/golang.org
%{__mkdir_p} %{buildroot}%{gopath}/src/gopkg.in
%{__mkdir_p} %{buildroot}%{gopath}/src/labix.org

%{__mkdir_p} %{buildroot}%{_rpmconfigdir}/macros.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gdbinit.d
cp -av %{SOURCE100} $RPM_BUILD_ROOT%{_sysconfdir}/gdbinit.d/golang.gdb
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/prelink.conf.d
cp -av %{SOURCE101} $RPM_BUILD_ROOT%{_sysconfdir}/prelink.conf.d/golang.conf

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cat > %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh << EOF
export GOROOT="%{goroot}"
export GOPATH="%{gopath}"
export PATH=\$PATH:\${GOROOT}/bin:\${GOPATH}/bin
export gohostarch=amd64
EOF
chmod a+x %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh

%post bin
%{_sbindir}/update-alternatives --install %{_bindir}/go go %{goroot}/bin/go 90 --slave %{_bindir}/gofmt gofmt %{goroot}/bin/gofmt

%preun bin
%{_sbindir}/update-alternatives --remove go %{goroot}/bin/go

%clean
#[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
#[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
#[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%dir %{goroot}/doc
%doc %{goroot}/doc/*
%dir %{goroot}
%dir %{gopath}
%dir %{gopath}/src
%dir %{gopath}/src/github.com
%dir %{gopath}/src/bitbucket.org
%dir %{gopath}/src/code.google.com
%dir %{gopath}/src/golang.org
%dir %{gopath}/src/gopkg.in
%dir %{gopath}/src/labix.org
%{goroot}
%{gopath}
%{goroot}/*
%{gopath}/*

#%{gopath}/api
#%{gopath}/AUTHORS
#%{gopath}/bin
#%{gopath}/CONTRIBUTORS
#%{gopath}/favicon.ico
#%{gopath}/LICENSE
#%{gopath}/PATENTS
#%{gopath}/robots.txt
#%{gopath}/VERSION.cache

#%dir %{gopath}/src
#%dir %{goroot}/doc
#%dir %{goroot}/pkg
#%dir %{goroot}/bin
#%dir %{goroot}/misc
#%dir %{goroot}/test
#%dir %{goroot}/lib
%exclude %{gopath}/src
%exclude %{goroot}/doc
%exclude %{goroot}/misc
%exclude %{goroot}/test
%exclude %{goroot}/lib
%exclude %{goroot}/pkg
%exclude %{goroot}/bin

%{_sysconfdir}/gdbinit.d
%{_sysconfdir}/prelink.conf.d
%{_sysconfdir}/profile.d

%files -f %{name}-%{version}/go-src.list src

%files -f %{name}-%{version}/go-docs.list docs

%files -f %{name}-%{version}/go-misc.list misc

%files -f %{name}-%{version}/go-tests.list tests

%files -f %{name}-%{version}/go-pkg.list bin

%files -f %{name}-%{version}/go-shared.list shared

%changelog
