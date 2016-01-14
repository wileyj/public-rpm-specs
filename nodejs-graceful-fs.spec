%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-graceful-fs
Version:    1.1.8
Release:    3.%{dist}
Summary:    'fs' module with incremental back-off on EMFILE
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      Development/Libraries
URL:        https://github.com/isaacs/node-graceful-fs
Source0:    http://registry.npmjs.org/graceful-fs/-/graceful-fs-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel
Requires:       nodejs

%description
Just like node.js' fs module, but it does an incremental back-off when EMFILE is
encountered.  Useful in asynchronous situations where one needs to try to open
lots and lots of files.

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/graceful-fs
cp -p graceful-fs.js package.json %{buildroot}%{nodejs_libdir}/graceful-fs

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/graceful-fs
%doc README.md

%changelog
