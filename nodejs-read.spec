%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-read
Version:    0.0.2
Release:    3.%{dist}
Summary:    read(1) for node programs
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      Development/Libraries
URL:        https://github.com/isaacs/read
Source0:    http://registry.npmjs.org/read/-/read-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel
Requires:       nodejs

%description
read(1)

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/read
cp -pr lib package.json %{buildroot}%{nodejs_libdir}/read

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/read
%doc README.md example

%changelog
