Name:           ruby-rpm-macros
Version:        2.4.0
Release:        11.%{?dist}
Summary:        The unversioned Python RPM macros

License:        MIT
Source0:        macros.ruby
Source1:        macros.rubygems
BuildArch:      noarch

%description
This package contains the unversioned RUby RPM macros, that most
implementations should rely on.

You should not need to install this package manually as the various
ruby?-devel packages require it. So install a ruby-devel package instead.

%package -n rubygem-rpm-macros
Summary:        RPM macros for building rubygem packages

%description -n rubygem-rpm-macros
RPM macros for building rubygem packages


%prep

%build

%install
mkdir -p %{buildroot}/%{_rpmconfigdir}/macros.d/
install -m 644 %{SOURCE0} %{SOURCE1} %{buildroot}/%{_rpmconfigdir}/macros.d/


%files
%{_rpmconfigdir}/macros.d/macros.ruby

%files -n rubygem-rpm-macros
%{_rpmconfigdir}/macros.d/macros.rubygems


%changelog
