%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-compat-symlinks
Version:    1
Release:    3.%{dist}
Summary:    Compatibility symlinks for Node.js modules
License:    Public Domain
Vendor: %{vendor}
Packager: %{packager}
Group:      Development/Languages
URL:        http://nodejs.tchol.org/
# downloaded from https://github.com/isaacs/node-tap/tarball/9d7cd989c77b39ccd58ce147e2fe86ca5aeafe0e
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch
Conflicts:  node

BuildRequires:  nodejs-devel
Requires:       nodejs  nodejs-devel

%description
This contains compatibility symlinks for Node modules and applications that
expect Node's binaries and directories to be called "node" instead of "nodejs".

This package and the "node" package cannot be installed at the same time because
many files will conflict.

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}

ln -s ./nodejs %{buildroot}%{_bindir}/node
ln -s ./nodejs %{buildroot}%{_includedir}/node

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{_bindir}/node
%{_includedir}/node

%changelog
