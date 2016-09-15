%define repo https://github.com/apache/ant
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">vr'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1`)
%define rel_version 1

%define _javadir /usr/java
%define ant_prefix /opt/%{name}

Name:           ant
Summary:        software project management tool
Version:        %{gitversion}
Release:        %{rel_version}.%{revision}.%{dist}
Url:            http://ant.apache.org
License:        Apache
Vendor: 	%{vendor}
Packager: 	%{packager}
Group:          Application/Web

%description
Apache Ant is a Java-based build tool. In theory, it is kind of like make, without make's wrinkles

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
source /etc/profile

%build
cd %{name}-%{version}
export ANT_HOME=%{buildroot}%{ant_prefix}-%{version}

%install
cd %{name}-%{version}
%{__mkdir_p} %{buildroot}/etc/profile.d
%{__mkdir_p} %{buildroot}/etc/ld.so.conf.d
%{__mkdir_p} %{buildroot}/%{_bindir}
%{__mkdir_p} %{buildroot}%{ant_prefix}-%{version}
sh build.sh

cat <<EOF> %{buildroot}/etc/profile.d/%{name}.sh
export PATH="$PATH:%{ant_prefix}-%{version}/bin"
EOF

cat <<EOF> %{buildroot}/etc/ld.so.conf.d/%{name}.conf
%{ant_prefix}-%{version}/lib"
EOF

cp -R dist/bin %{buildroot}%{ant_prefix}-%{version}
cp -R dist/lib %{buildroot}%{ant_prefix}-%{version}
%__ln_s -f %{ant_prefix}-%{version} %{buildroot}%{ant_prefix}
%__ln_s -f %{ant_prefix}-%{version}/bin/%{name} %{buildroot}%{_bindir}/%{name}

%post
ldconfig 

%postun
ldconfig

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
[ "%{_builddir}/%{realname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{realname}-%{version}
[ "%{_builddir}/%{realname}" != "/" ] && %__rm -rf %{_builddir}/%{realname}

%files
%defattr(-,root,root)
%dir %{ant_prefix}-%{version}
%{ant_prefix}-%{version}/*
%{ant_prefix}
%{_bindir}/%{name}
/etc/profile.d/%{name}.sh
/etc/ld.so.conf.d/ant.conf
