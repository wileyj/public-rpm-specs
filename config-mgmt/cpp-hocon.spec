%define repo https://github.com/puppetlabs/cpp-hocon
%define gitversion %(echo `curl -s  %{repo}/releases | grep 'class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

Name:           cpp-hocon
Version:        %{gitversion}
Release:        %{rel_version}.%{revision}.%{dist}
Summary:        This is a port of the TypesafeConfig library to C++.
Group:          Development/Libraries/C and C++
License:        ASL 2.0
Vendor: 	%{vendor}
Packager: 	%{packager}
URL:            https://puppetlabs.com/%{name}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: boost-devel >= 1.59,  curl, curl-devel, leatherman, leatherman-devel
Requires:	boost >= 1.59, leatherman, curl
BuildArch:	noarch

%description
This is a port of the TypesafeConfig library to C++.

%package devel
Summary:        This is a port of the TypesafeConfig library to C++.
Group:          Development/Libraries/C and C++
Requires:       %{name}

%description devel
Development files for cpp-hocon


%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}


%install
cd %{name}-%{version}
rm -rf %{buildroot}
mkdir release && cd release
%{__mkdir_p} %{buildroot}%{_includedir}
cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_CXX_FLAGS="-I /usr/include/leatherman/vendor" ..
make
make DESTDIR=%{buildroot} INSTALL="install -p" install
%__mv %{buildroot}/usr/lib %{buildroot}%{_libdir}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}


%files
%defattr(-,root,root,-)
%{_libdir}/libcpp-hocon.a

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/hocon
%{_includedir}/hocon/config.hpp
%{_includedir}/hocon/config_exception.hpp
%{_includedir}/hocon/config_include_context.hpp
%{_includedir}/hocon/config_includer.hpp
%{_includedir}/hocon/config_includer_file.hpp
%{_includedir}/hocon/config_list.hpp
%{_includedir}/hocon/config_mergeable.hpp
%{_includedir}/hocon/config_object.hpp
%{_includedir}/hocon/config_origin.hpp
%{_includedir}/hocon/config_parse_options.hpp
%{_includedir}/hocon/config_parseable.hpp
%{_includedir}/hocon/config_render_options.hpp
%{_includedir}/hocon/config_resolve_options.hpp
%{_includedir}/hocon/config_syntax.hpp
%{_includedir}/hocon/config_value.hpp
%{_includedir}/hocon/config_value_factory.hpp
%{_includedir}/hocon/export.h
%{_includedir}/hocon/functional_list.hpp
%{_includedir}/hocon/parser/config_document.hpp
%{_includedir}/hocon/parser/config_document_factory.hpp
%{_includedir}/hocon/parser/config_node.hpp
%{_includedir}/hocon/path.hpp
%{_includedir}/hocon/program_options.hpp
%{_includedir}/hocon/types.hpp
%{_includedir}/hocon/version.h
%changelog
