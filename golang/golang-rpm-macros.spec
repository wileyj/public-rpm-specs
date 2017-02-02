Name:           golang-rpm-macros
Version:        1.8.0
Release:        11.%{?dist}
Summary:        The unversioned golang rpm macros
Provides: 	golang-srpm-macros

License:        MIT
Source0:        macros.golang
BuildArch:      noarch

%description
This package contains the unversioned golang RPM macros, that most implementations should rely on.


%prep

%build

%install
mkdir -p %{buildroot}/%{_rpmconfigdir}/macros.d/
install -m 644 %{SOURCE0} %{buildroot}/%{_rpmconfigdir}/macros.d/


%files
%{_rpmconfigdir}/macros.d/macros.golang

%changelog
