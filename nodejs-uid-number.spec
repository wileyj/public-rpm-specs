%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-uid-number
Version:    0.0.3
Release:    3.%{dist}
Summary:    Convert a username/group name to a UID/GID number
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/uid-number
Source0:    http://registry.npmjs.org/uid-number/-/uid-number-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel


Requires:       nodejs


%description
uid-number

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/uid-number
cp -pr *.js package.json %{buildroot}%{nodejs_libdir}/uid-number

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/uid-number
%doc README.md

%changelog
