%define filelist %{name}-%{version}-filelist
%global sensu_base /etc/sensu
%global plugins    %{sensu_base}/plugins
%global metrics    %{sensu_base}/metrics
%global handlers   %{sensu_base}/handlers
%global extensions %{sensu_base}/extensions
%global mutators   %{sensu_base}/mutators

%global gem_name sensu-plugins-disk-checks
%define repo https://rubygems.org/api/v1/gems
%global gem_version %(echo `curl %{repo}/%{gem_name}.json | jq '.version' | tr -d '"'`)
%global gem_summary %( echo ` curl %{repo}/%{gem_name}.json | jq '.info' | sed -e 's/\\n/ /g' | tr -d '"'`)

Name: rubygem-%{gem_name}
Version: %{gem_version}
Release: 1.%{dist}
Summary: %{gem_summary}
Group: Development/Languages
License: Ruby
Vendor: %{vendor}
Packager: %{packager}
Requires: ruby rubygems 
BuildRequires: rubygems rubygems-devel
BuildRequires: ruby ruby-devel
#BuildRequires:  rubygem-rpm-macros
#BuildRequires:  ruby-rpm-macros
Provides: rubygem-%{gem_name}
Provides: rubygem(%{gem_name})
Obsoletes: rubygem-%{gem_name} < %{version}
Obsoletes: rubygem(%{gem_name}) < %{version}
Requires: rubygem-sensu-plugin
Requires: rubygem-json

%description
%{summary}

%prep
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install --install-dir %{_builddir}/%{name}/%{gem_dir} --bindir %{_builddir}/%{name}/%{_bindir} --force --no-rdoc --no-ri --no-doc --ignore-dependencies %{gem_name}

%build

%install
find %{_builddir}/%{name} -type f -exec sed -i -e 's|/usr/local/bin/ruby|/usr/bin/ruby|g' {} \;
cp -pa %{_builddir}/%{name}/* %{buildroot}/
for file in `ls  %{buildroot}%{_bindir}`
do
    if [[ $file == metric* ]]; then
        if [ ! -d %{buildroot}%{metrics} ];then
            %__mkdir_p %{buildroot}%{metrics}
        fi
        %__mv %{buildroot}%{_bindir}/$file %{buildroot}%{metrics}
    elif [[ $file == check* ]]; then
        if [ ! -d %{buildroot}%{plugins} ];then
            %__mkdir_p %{buildroot}%{plugins}
        fi
        %__mv %{buildroot}%{_bindir}/$file %{buildroot}%{plugins}
    elif [[ $file == mutator* ]]; then
        if [ ! -d %{buildroot}%{mutators} ];then
            %__mkdir_p %{buildroot}%{mutators}
        fi
        %__mv %{buildroot}%{_bindir}/$file %{buildroot}%{mutators}
    elif [[ $file == handle* ]]; then
        if [ ! -d %{buildroot}%{handlers} ];then
            %__mkdir_p %{buildroot}%{handlers}
        fi
        %__mv %{buildroot}%{_bindir}/$file %{buildroot}%{handlers}
    else
        if [ ! -d %{buildroot}%{plugins} ];then
            %__mkdir_p %{buildroot}%{plugins}
        fi
        %__mv %{buildroot}%{_bindir}/$file %{buildroot}%{plugins}
    fi
done
%__rm -rf %{buildroot}%{_bindir}

echo "%{gem_dir}/*" >> %{filelist}
if [ -d %{buildroot}%{metrics} ];then
  echo "%{metrics}/*" >> %{filelist}
fi
if [ -d %{buildroot}%{plugins} ];then
  echo "%{plugins}/*" >> %{filelist}
fi
if [ -d %{buildroot}%{handlers} ];then
  echo "%{handlers}/*" >> %{filelist}
fi
if [ -d %{buildroot}%{extensions} ];then
  echo "%{extenstions}/*" >> %{filelist}
fi
if [ -d %{buildroot}%{mutators} ];then
  echo "%{mutators}/*" >> %{filelist}
fi
if [ -f %{buildroot}%{gem_dir}/specifications/%{gemname}-%{version}.gemspec ]
then
    echo "Making changes using sed to %{buildroot}%{gem_dir}/specifications/%{gemname}-%{version}.gemspec"
    sed -i -e 's|\["= |\[">= |g' %{buildroot}%{gem_dir}/specifications/%{gemname}-%{version}.gemspec
fi
if [ -f %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/%{gemname}.gemspec ]
then
    echo "Making changes using sed to %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/%{gemname}.gemspec"
    sed -i -e 's|\["= |\[">= |g' %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/%{gemname}.gemspec
fi
%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{filelist}" != "/" ] && %__rm -rf %{_builddir}/%{filelist}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files -f %{filelist}
