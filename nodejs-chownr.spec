%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-chownr
Version:    0.0.1
Release:    3.%{dist}
Summary:    Like `chown -R`
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/chownr
Source0:    http://registry.npmjs.org/chownr/-/chownr-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel
Requires:       nodejs

%description
chownr

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/chownr
cp -p chownr.js package.json %{buildroot}%{nodejs_libdir}/chownr

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/chownr
%doc README.md

%changelog
