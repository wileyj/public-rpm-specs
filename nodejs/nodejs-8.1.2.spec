%define repo https://github.com/nodejs/node
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d 'v\\-</span class="tag-name">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1
%define _base node

Name:          nodejs
Version:       %{gitversion}
Release:       %{revision}.%{dist}
Summary:       Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
Group:         Development/Libraries
License:       MIT License
Vendor: %{vendor}
Packager: %{packager}
URL:           http://nodejs.org
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-tmp
Prefix:        /usr
BuildRequires: tar
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: openssl-devel => 1.1
BuildRequires: libstdc++-devel
BuildRequires: zlib-devel
BuildRequires: gzip
Provides: %{name} = %{version}
Patch0: node-js.centos5.configure.patch

%description
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.

%package binary
Summary:       Node.js build binary tarballs
Group:         Development/Libraries
License:       MIT License
URL:           http://nodejs.org

%description binary
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.

%package npm
Summary:       Node Packaged Modules
Group:         Development/Libraries
License:       MIT License
URL:           http://nodejs.org
Obsoletes:     npm
Provides:      npm
Requires:      %{name} = %{version}

%description npm
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.

%package devel
Summary:       Header files for %{name}
Group:         Development/Libraries
Requires:      %{name}

%description devel
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}


%build
cd %{name}-%{version}
%define _node_arch %{nil}
%define _node_arch x64
if [ -z %{_node_arch} ];then
  echo "bad arch"
  exit 1
fi
for file in `ls doc/api`; do 
  sed -i -e 's/REPLACEME/%{version}/g' doc/api/$file
done

./configure \
    --prefix=/usr \
    --shared-openssl \
    --shared-openssl-includes=%{_includedir} \
    --shared-zlib \
    --shared-zlib-includes=%{_includedir}
make -j4


%install
cd %{name}-%{version}
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
cd %{buildroot}
%__mkdir_p %{buildroot}/usr/share/%{_base}js
tar -cf %{_builddir}/%{_base}-v%{version}-linux-%{_node_arch}.tar %{buildroot}/*
gzip %{_builddir}/%{_base}-v%{version}-linux-%{_node_arch}.tar 
%__mv %{_builddir}/%{_base}-v%{version}-linux-%{_node_arch}.tar.gz %{buildroot}/usr/share/%{_base}js/

# prefix all manpages with "npm-"
pushd $RPM_BUILD_ROOT/usr/lib/node_modules/npm/man/
for dir in *; do
    mkdir -p $RPM_BUILD_ROOT/usr/share/man/$dir
    pushd $dir
    for page in *; do
        if [[ $page != npm* ]]; then
        mv $page npm-$page
    fi
    done
    popd
    cp $dir/* $RPM_BUILD_ROOT/usr/share/man/$dir
done
popd

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}


%files
%defattr(-,root,root,-)
%{_prefix}/share/doc/%{_base}
%{_prefix}/share/systemtap/tapset/%{_base}.stp

%defattr(755,root,root)
%{_bindir}/node

%doc
/usr/share/man/man1/node.1.gz

%files binary
%defattr(-,root,root,-)
%{_prefix}/share/%{_base}js/%{_base}-v%{version}-linux-%{_node_arch}.tar.gz

%files npm
%defattr(-,root,root,-)
%{_prefix}/lib/node_modules/npm
%{_bindir}/npm

%doc
/usr/share/man/man1/npm*
/usr/share/man/man5/npm*
/usr/share/man/man7/npm*

%files devel
%{_includedir}/node/

%changelog

