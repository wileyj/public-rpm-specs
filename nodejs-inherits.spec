%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-inherits
Version:    1.0.0
Release:    3.%{dist}
Summary:    A tiny simple way to do classic inheritance in js
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      Development/Libraries
URL:        https://github.com/isaacs/inherits
Source0:    http://registry.npmjs.org/inherits/-/inherits-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel
Requires:       nodejs

%description
inheritence module for nodejs

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/inherits
cp -pr inherits.js package.json %{buildroot}%{nodejs_libdir}/inherits

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/inherits
%doc README.md

%changelog
