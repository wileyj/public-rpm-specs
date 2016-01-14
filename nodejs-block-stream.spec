%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-block-stream
Version:    0.0.5
Release:    3.%{dist}
Summary:    A stream of blocks
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      Development/Libraries
URL:        https://github.com/isaacs/block-stream
Source0:    http://registry.npmjs.org/block-stream/-/block-stream-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel

%description
%{summary}.

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/block-stream
cp -pr block-stream.js package.json %{buildroot}%{nodejs_libdir}/block-stream

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/block-stream
%doc README.md

%changelog
