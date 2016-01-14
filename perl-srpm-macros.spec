Name:           perl-srpm-macros
Version:        1
Release:        1.%{?dist}
Summary:        RPM macros for building Perl packages for various architectures
Group:          Development/Libraries
License:        GPLv3+
Source0:        macros.perl
BuildArch:      noarch
# for install command
BuildRequires:  coreutils
Provides: %{name}

%description
The package provides macros for building projects in perl
on various architectures.

%prep
# nothing to prep, just for hooks

%build
# nothing to build, just for hooks

%install
install -m 644 -D "%{SOURCE0}" \
    '%{buildroot}%{_rpmconfigdir}/macros.d/macros.perl'

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%{_rpmconfigdir}/macros.d/macros.perl

%changelog