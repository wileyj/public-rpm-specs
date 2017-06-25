Name:           python-rpm-macros
Version:        4
Release:        1.%{?dist}
Summary:        The unversioned Python RPM macros

License:        MIT
Source0:        macros.python
Source1:        macros.python-srpm
Source2:        macros.python2
Source3:        macros.python3

BuildArch:      noarch
# For %%python3_pkgversion used in %%python_provide
Requires:       python-srpm-macros

%description
This package contains the unversioned Python RPM macros, that most
implementations should rely on.

You should not need to install this package manually as the various
python?-devel packages require it. So install a python-devel package instead.

%package -n python-srpm-macros
Summary:        RPM macros for building Python source packages
Provides:	python3-srpm-macros

%description -n python-srpm-macros
RPM macros for building Python source packages.

%package -n python2-rpm-macros
Summary:        RPM macros for building Python 2 packages

%description -n python2-rpm-macros
RPM macros for building Python 2 packages.

%package -n python3-rpm-macros
Summary:        RPM macros for building Python 3 packages

%description -n python3-rpm-macros
RPM macros for building Python 3 packages.


%prep

%build

%install
mkdir -p %{buildroot}/%{_rpmconfigdir}/macros.d/
install -m 644 %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} \
  %{buildroot}/%{_rpmconfigdir}/macros.d/


%files
%{_rpmconfigdir}/macros.d/macros.python

%files -n python-srpm-macros
%{_rpmconfigdir}/macros.d/macros.python-srpm

%files -n python2-rpm-macros
%{_rpmconfigdir}/macros.d/macros.python2

%files -n python3-rpm-macros
%{_rpmconfigdir}/macros.d/macros.python3


%changelog
