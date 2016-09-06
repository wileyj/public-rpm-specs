%define repo https://github.com/technomancy/leiningen.git
%define gitversion %(echo `curl -s https://github.com/technomancy/leiningen/releases | grep 'css-truncate-target' | head -1 |  tr -d '\\-</span class="css-truncate-target">'`)
%define lein_dir /opt/%{name}
Name:           leiningen
Version:        %{gitversion}
Release:        1.%{dist}
Summary:        A network tool for managing many disparate systems
License:        ASL 2.0
Packager:       %{packager}
Vendor:         %{vendor}
URL:            https://leiningen.org
Group:          System Environment/Base
Requires:       jdk
BuildArch:      noarch

%description
Automate Clojure projects without setting your hair on fire. https://leiningen.org

#%prep
#if [ -d %{name}-%{version} ];then
#    rm -rf %{name}-%{version}
#fi
#git clone %{repo} %{name}-%{version}
#cd %{name}-%{version}
#git submodule init
#git submodule update

#%build
#cd %{name}-%{version}

%install
#cd %{name}-%{version}
#rm -rf %{buildroot}
#%__mkdir_p %{buildroot}%{lein_dir}
%__mkdir_p %{buildroot}%{_bindir}
curl https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein -o %{buildroot}%{_bindir}/lein
#cp -pR . %{buildroot}%{lein_dir}
chmod 755 %{buildroot}%{_bindir}/lein
#chmod 755 %{buildroot}%{lein_dir}/bin/lein-pkg
#ln -s %{lein_dir}/bin/lein %{buildroot}%{_bindir}/lein

#%post
#%{_bindir}/lein

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-, root, root, 0755)
#%{lein_dir}
%{_bindir}/lein

%changelog

