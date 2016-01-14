#AutoReqProv: no
#  gem list ^json$ -r |  cut -f2 -d" " | grep -o '\((.*\)$' | tr -d '()'
%include %{_rpmconfigdir}/macros.d/macros.rubygems
%global gemname hiera
%global remoteversion %(echo `gem list ^%{gemname}$ -r |  grep %{gemname} | cut -f2 -d" " | tr -d '()' | tr -d ','`)
%global rubyabi 2.2.2
%global puppet_base /etc/puppetlabs
%global binpath /opt/puppetlabs/bin
%global codedir %{puppet_base}/code
%global hieradata %{codedir}/hieradata

Summary: Light weight hierarchical data store
Name: %{gemname}
Version: %{remoteversion}
Release: 1.%{dist}
Group: Development/Languages
License: Ruby
Vendor: %{vendor}
Packager: %{packager}
Requires: ruby rubygems puppet
Requires: rubygem-json_pure
BuildRequires: rubygems rubygems-devel
BuildRequires: ruby
BuildArch: x86_64
Provides: rubygem-%{gemname}
Provides: rubygem(%{gemname})
Provides: %{gemname}

%description
A pluggable data store for hierarcical data.


%prep

%setup -q -c -T
%__mkdir_p %{_builddir}/%{name}%{gem_dir}
%__mkdir_p %{_builddir}/%{name}%{_bindir}

export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install --install-dir %{_builddir}/%{name}%{gem_dir} --bindir %{_builddir}/%{name}%{_bindir} --force --no-rdoc --no-ri --no-doc --ignore-dependencies %{gemname}

%build

%install
find %{_builddir}/%{name} -type f -exec sed -i -e 's|/usr/local/bin/ruby|/usr/bin/ruby|g' {} \;

cp -pa %{_builddir}/%{name}/* %{buildroot}/
%__mkdir_p %{buildroot}/%{binpath}
ln -sf %{_bindir}/%{name} ${RPM_BUILD_ROOT}%{binpath}/%{name}

%__mkdir_p %{buildroot}/%{hieradata}
cat <<EOF> %{buildroot}%{codedir}/hiera.yaml
---
:logger: console

:backends:
    - yaml

:yaml:
    :datadir: /etc/puppetlabs/code/hieradata

:hierarchy:
    - "sites/%{::site_name}"
    - "hosts/%{::hostname_full}"
    - "environment/%{::env_name}"
    - "%{::domain}"
    - "region/%{::region_short}"
    - "roles/%{::server_role}"
    - "users/%{::server_role}"
    - "users/admins"
    - "users/analytics"
    - "users/celery"
    - "users/dev"
    - "users/jenkins"
    - "users/postgres"
    - "users/subversion"
    #- "users/monitoring"
    - "os/%{::osfamily}"
    - common
    #- monitoring

:merge_behavior: deeper
EOF

find %{_builddir}/%{name} -type f -exec sed -i -e 's|/usr/local/bin/ruby|/usr/bin/ruby|g' {} \; 
cp -pa %{_builddir}/%{name}/* %{buildroot}/
if [ -f *.gemspec ]
then
    sed -e '/s.installed_by_version/ s/^#*/#/' -i  *.gemspec
fi
(
    cd %{buildroot}
    echo '%defattr(-,root,root,-)'
    if [ -d %{buildroot}%{gem_dir}/cache ]
    then
        echo '%exclude "%{gem_dir}/cache"'
    fi
    if [ -f %{buildroot}%{gem_dir}/cache/%{gemname}-*.gem ]
    then
        echo '%exclude "%{gem_dir}/cache/%{gemname}-*.gem"'
    fi
    if [ -f %{buildroot}%{gem_dir}/gems/%{gemname}-*/.gitignore ]
    then
        echo '%exclude "%{gem_dir}/gems/%{gemname}-*/.gitignore"'
    fi
    if [ -f %{buildroot}%{gem_dir}/gems/%{gemname}-*/.travis.yml ]
    then
        echo '%exclude "%{gem_dir}/gems/%{gemname}-*/.travis.yml"'
    fi
    if [ -f %{buildroot}%{gem_dir}/gems/%{gemname}-*/.yardopts ]
    then
        echo '%exclude "%{gem_dir}/gems/%{gemname}-*/.yardopts"'
    fi
    echo "%{codedir}/%{name}.yaml"
    echo "%{binpath}/%{name}"
    find %{buildroot} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g' | %{__grep} -v '%{gem_dir}/cache'
    find %{buildroot} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g' | %{__grep} -v '%{gem_dir}/cache/%{gemname}-*.gem'
) > filelist
%{__sed} -i -e 's/%dir ""//g' filelist
%{__sed} -i -e 's|%dir "/usr"||' filelist
%{__sed} -i -e 's|%dir "%{_bindir}"||' filelist
%{__sed} -i -e 's|%dir "%{_datadir}"||' filelist
%{__sed} -i -e 's|%dir "%{gem_dir}"||' filelist
%{__sed} -i -e 's|%dir "%{gem_dir}/build_info"||' filelist
%{__sed} -i -e 's|%dir "%{gem_dir}/doc"||' filelist
%{__sed} -i -e 's|%dir "%{gem_dir}/extensions"||' filelist
%{__sed} -i -e 's|%dir "%{gem_dir}/gems"||' filelist
%{__sed} -i -e 's|%dir "%{gem_dir}/specifications"||' filelist
%{__sed} -i -e '/^$/d' filelist

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files -f filelist

