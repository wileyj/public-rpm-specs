%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-fast-list
Version:    1.0.2
Release:    3.%{dist}
Summary:    A fast linked list
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      Development/Libraries
URL:        https://github.com/isaacs/fast-list
Source0:    http://registry.npmjs.org/fast-list/-/fast-list-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel
Requires:       nodejs

%description
A fast linked list. (good for queues, stacks, etc.)

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/fast-list
cp -pr fast-list.js package.json %{buildroot}%{nodejs_libdir}/fast-list

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/fast-list
%doc README.md

%changelog
