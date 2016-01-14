%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-minimatch
Version:    0.2.4
Release:    3.%{dist}
Summary:    JavaScript glob matcher
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/minimatch
Source0:    http://registry.npmjs.org/minimatch/-/minimatch-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel
Requires:       nodejs

Requires:       nodejs-lru-cache >= 1.0.5

%description
Converts glob expressions to JavaScript "RegExp" objects.

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/minimatch
cp -p minimatch.js package.json %{buildroot}%{nodejs_libdir}/minimatch

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/minimatch
%doc README.md LICENSE

%changelog
