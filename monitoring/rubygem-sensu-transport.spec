%global _python_bytecompile_errors_terminate_build 0
%global gemname sensu-transport
%global repo https://github.com/sensu/%{gemname}.git
%global gemdesc %(echo `gem list ^%{gemname}$ -r -d | tail -1`)
%global remoteversion %(echo `gem list ^%{gemname}$ -r |  cut -f2 -d" " | tr -d '()'`)
%global sensu_base /etc/sensu
%global plugins    %{sensu_base}/plugins
%global metrics    %{sensu_base}/metrics
%global handlers   %{sensu_base}/handlers
%global extensions %{sensu_base}/extensions
%global mutators   %{sensu_base}/mutators
%include %{_rpmconfigdir}/macros.d/macros.rubygems

%define filelist %{name}-%{version}-filelist
Summary: %{gemdesc}
Name: rubygem-%{gemname}
Version: %{remoteversion}
Release: 1.%{dist}
Group: Development/Languages
License: Ruby
Vendor: %{vendor}
Packager: %{packager}
Requires: ruby rubygems
Requires: rubygem-sensu-em
Requires: rubygem-amqp
Requires: rubygem-em-redis-unified
BuildRequires: rubygems rubygems-devel
BuildRequires: ruby ruby-devel
BuildArch: x86_64
Provides: rubygem-%{gemname}
Provides: rubygem(%{gemname})

%description
%{summary}



%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
gem install --install-dir %{_builddir}/%{name}%{gem_dir} --bindir %{_builddir}/%{name}%{_bindir} --force --no-rdoc --no-ri --no-doc --ignore-dependencies %{gemname}

%build

%install
cd %{name}-%{version}
%__mkdir_p %{_builddir}/%{name}%{gem_dir}
%__mkdir_p %{_builddir}/%{name}%{_bindir}
find %{_builddir}/%{name} -type f -exec sed -i -e 's|/usr/local/bin/ruby|/usr/bin/ruby|g' {} \;
cp -pa %{_builddir}/%{name}/* %{buildroot}/
find %{_builddir}/%{name} -type f -exec sed -i -e 's|/usr/local/bin/ruby|/usr/bin/ruby|g' {} \; 
cp -pa %{_builddir}/%{name}/* %{buildroot}/
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
    find %{buildroot} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g' | %{__grep} -v '%{gem_dir}/cache'
    find %{buildroot} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g' | %{__grep} -v '%{gem_dir}/cache/%{gemname}-*.gem'
) >%{filelist}
%{__sed} -i -e 's|%dir "%{gem_dir}/specifications"||' %{filelist}
%{__sed} -i -e 's|%dir "%{_datadir}"||' %{filelist}
%{__sed} -i -e 's|%dir "%{gem_dir}"||' %{filelist}
%{__sed} -i -e 's|%dir "%{gem_dir}/build_info"||' %{filelist}
%{__sed} -i -e 's|%dir "%{gem_dir}/doc"||' %{filelist}
%{__sed} -i -e 's|%dir "%{gem_dir}/extensions"||' %{filelist}
%{__sed} -i -e 's|%dir "%{gem_dir}/gems"||' %{filelist}
%{__sed} -i -e 's|%dir "%{_exec_prefix}"||' %{filelist}
%{__sed} -i -e 's|%dir "%{_bindir}"||' %{filelist}
%{__sed} -i -e 's|%dir "%{_libdir}"||' %{filelist}
%{__sed} -i -e 's|%dir "%{_libdir}/gems"||' %{filelist}
%{__sed} -i -e 's|%dir "%{_libdir}/gems/ruby"||' %{filelist}
%{__sed} -i -e 's/%dir ""//g' %{filelist}
%{__sed} -i -e '/^$/d' %{filelist}

if [ -f %{buildroot}%{gem_dir}/specifications/%{gemname}-%{version}.gemspec ]
then
    echo "Making changes using sed to %{buildroot}%{gem_dir}/specifications/%{gemname}-%{version}.gemspec"
    %{__sed} -i -e 's|\["= |\[">= |g' %{buildroot}%{gem_dir}/specifications/%{gemname}-%{version}.gemspec

fi
if [ -f %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/%{gemname}.gemspec ]
then
    echo "Making changes using sed to %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/%{gemname}.gemspec"
    %{__sed} -i -e 's|\["= |\[">= |g' %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/%{gemname}.gemspec
    %{__sed} -i -e 's|("sensu-em".*| "sensu-em"|g' %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/%{gemname}.gemspec
    %{__sed} -i -e 's|("amqp".*| "amqp"|g' %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/%{gemname}.gemspec
    %{__sed} -i -e 's|("em-redis-unified".*| "em-redis-unified"|g' %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/%{gemname}.gemspec
fi

if [ -f %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/lib/sensu/transport/rabbitmq.rb ]
then
     %{__sed} -i -e 's|"amqp".*|"amqp"|g' %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/lib/sensu/transport/rabbitmq.rb
fi

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files -f %{name}-%{version}/%{filelist}