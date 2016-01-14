%global apachedir /opt/apache
%define mmn 20120211
%{!?_httpd_apxs: %{expand: %%global _httpd_apxs %{apachedir}/bin/apxs}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
# https://github.com/GrahamDumpleton/mod_wsgi/releases/tag/3.5
%global commit d9d5fea585b23991f76532a9b07de7fcd3b649f4
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           mod_wsgi
Version:        3.5
Release:        1.%{dist}
Summary:        A WSGI interface for Python web applications in Apache
Group:          System Environment/Libraries
License:        ASL 2.0
Vendor: %{vendor}
Packager: %{packager}
URL:            http://modwsgi.org
Source0:        https://github.com/GrahamDumpleton/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
Source1:        wsgi.conf
Source2:        wsgi-python3.conf

BuildRequires:  httpd-devel, python-devel, autoconf
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif
Requires:       httpd-mmn  = %{mmn}

# Suppress auto-provides for module DSO
%{?filter_provides_in: %filter_provides_in %{_httpd_moddir}/.*\.so$}
%{?filter_setup}


%if 0%{?with_python3}
%package -n python3-%{name}
Summary:        A WSGI interface for Python3 web applications in Apache
Group:          System Environment/Libraries
Requires:       httpd-mmn = %{mmn}

%description -n python3-%{name}
The mod_wsgi adapter is an Apacheache module that provides a WSGI compliant
interface for hosting Python based web applications within Apache. The
adapter is writtentten completely in C code against the Apache C runtime and
for hosting WSGI applications within Apache has a lower overhead than using
existing WSGI adapters for mod_python or CGI.
%endif

%description
The mod_wsgi adapter is an Apache module that provides a WSGI compliant
interface for hosting Python based web applications within Apache. The
adapter is written completely in C code against the Apache C runtime and
for hosting WSGI applications within Apache has a lower overhead than using
existing WSGI adapters for mod_python or CGI.


%prep
%setup -qn %{name}-%{commit}

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif

%build
export LDFLAGS="$RPM_LD_FLAGS -L%{_libdir}"
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure --enable-shared --with-apxs=%{_httpd_apxs}
make %{?_smp_mflags}

%if 0%{?with_python3}
pushd %{py3dir}
%configure --enable-shared --with-apxs=%{_httpd_apxs} --with-python=python3
make %{?_smp_mflags}
popd
%endif

%install
# first install python3 variant and rename the so file
%if 0%{?with_python3}
pushd %{py3dir}
make install DESTDIR=$RPM_BUILD_ROOT LIBEXECDIR=%{_httpd_moddir}
mv  $RPM_BUILD_ROOT%{_httpd_moddir}/mod_wsgi{,_python3}.so

install -d -m 755 $RPM_BUILD_ROOT%{_httpd_modconfdir}
%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# httpd <= 2.2.x
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_httpd_confdir}/wsgi-python3.conf
%else
# httpd >= 2.4.x
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-wsgi-python3.conf
%endif
popd
%endif

make install DESTDIR=$RPM_BUILD_ROOT LIBEXECDIR=%{_httpd_moddir}

install -d -m 755 $RPM_BUILD_ROOT%{_httpd_modconfdir}
%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# httpd <= 2.2.x
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}/wsgi.conf
%else
# httpd >= 2.4.x
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-wsgi.conf
%endif

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%doc LICENCE README
%config(noreplace) %{_httpd_modconfdir}/*wsgi.conf
%{_httpd_moddir}/mod_wsgi.so

%if 0%{?with_python3}
%files -n python3-%{name}
%doc LICENCE README
%config(noreplace) %{_httpd_modconfdir}/*wsgi-python3.conf
%{_httpd_moddir}/mod_wsgi_python3.so
%endif

%changelog
