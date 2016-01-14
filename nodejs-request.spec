%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-request
Version:    2.9.202
Release:    3.%{dist}
Summary:    Simplified HTTP request client
License:    ASL 2.0
Vendor: %{vendor}
Packager: %{packager}
Group:      Development/Libraries
URL:        https://github.com/mikeal/request
Source0:    http://registry.npmjs.org/request/-/request-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel

Requires:       nodejs

%description
request

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/request
cp -pr *.js vendor package.json %{buildroot}%{nodejs_libdir}/request

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/request
%doc README.md LICENSE

%changelog
