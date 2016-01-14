%if 0%{?el6}
    %define macro %{_rpmconfigdir}/macros.d/macros.python27
    %global __python /usr/bin/python27
%else
    %define macro %{_rpmconfigdir}/macros.d/macros.python
    %global __python /usr/bin/python
%endif

%include %{macro}

Name:           gyp
Version:        4.9.79
Release:        1.%{dist}
Summary:        GYP is a Meta-Build system
Group:          Development/Languages
License:        GPL
Packager: 	%{packager}
Vendor: 	%{vendor}
URL:            https://gyp.gsrc.io/
Source0:        %{name}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if 0%{?el6}
BuildRequires:  python27-devel
BuildRequires:  python27-setuptools
Requires:       python27
%else
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python
%endif

%description
GYP is intended to support large projects that need to be built on multiple platforms (e.g., Mac, Windows, Linux), and where it is important that the project can be built using the IDEs that are popular on each platform as if the project is a “native” one.

It can be used to generate XCode projects, Visual Studio projects, Ninja build files, and Makefiles. In each case GYP’s goal is to replicate as closely as possible the way one would set up a native build of the project using the IDE.

GYP can also be used to generate “hybrid” projects that provide the IDE scaffolding for a nice user experience but call out to Ninja to do the actual building (which is usually much faster than the native build systems of the IDEs).

%prep
%setup -q -n %{name}

%build
%{__python27} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python27} setup.py install --skip-build --root $RPM_BUILD_ROOT

 
%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root,-)
%{python27_sitelib}/%{name}/
%{python27_sitelib}/%{name}*.egg-info
%{_bindir}/gyp*

%changelog

