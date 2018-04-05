AutoReqProv: no
%global ruby_ver 2.4
%global alinux_ruby 24
%global gem_dir %{gem24_dir}



%define filelist %{name}-%{version}-filelist
%global sensu_base %{_sysconfdir}/sensu
%global plugins    %{sensu_base}/plugins
%global metrics    %{sensu_base}/metrics
%global handlers   %{sensu_base}/handlers
%global extensions %{sensu_base}/extensions
%global mutators   %{sensu_base}/mutators

%global gem_name sensu-plugins-aws
Name: rubygem%{alinux_ruby}-sensu-plugins-aws
Version: 10.0.3
Release: 1.%{dist}
AutoReqProv : no
Summary: rubygem sensu-plugins-aws
Group: Development/Languages
License: MIT
URL: https://github.com/sensu-plugins/sensu-plugins-aws
Vendor: %{vendor}
Packager: %{packager}
Requires: ruby%{alinux_ruby} rubygems%{alinux_ruby}
Requires: rubygem%{alinux_ruby}-sensu
Provides: rubygem%{alinux_ruby}-sensu-plugins-aws = %{version}
Provides: rubygem%{alinux_ruby}(sensu-plugins-aws) = %{version}
Obsoletes: rubygem%{alinux_ruby}-sensu-plugins-aws < %{version}
Obsoletes: rubygem%{alinux_ruby}(sensu-plugins-aws) < %{version}


Requires: rubygem%{alinux_ruby}-aws-sdk  >= 2.10
Requires: rubygem%{alinux_ruby}-aws-sdk-v1  >= 1.66.0
Requires: rubygem%{alinux_ruby}-erubis  >= 2.7.0
Requires: rubygem%{alinux_ruby}-fog  >= 1.32.0
Requires: rubygem%{alinux_ruby}-fog-core  >= 1.43.0
Requires: rubygem%{alinux_ruby}-rest-client  >= 1.8.0
Requires: rubygem%{alinux_ruby}-right_aws  >= 3.1.0
Requires: rubygem%{alinux_ruby}-sensu-plugin  >= 2.0


%description
This plugin provides native AWS instrumentation
for monitoring and metrics collection, including:
health and metrics for various AWS services, such
as EC2, RDS, ELB, and more, as well as handlers
for EC2, SES, and SNS.

%prep
%build
%install
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install --install-dir %{buildroot}/%{gem_dir} --bindir %{buildroot}/%{_bindir} --force --no-rdoc --no-ri --no-doc --ignore-dependencies %{gem_name} -v %{version}
if [ -d "%{buildroot}%{gem_dir}/extensions/x86_64-linux/2.4.0/%{gem_name}-%{version}" ]; then
%__mkdir_p %{buildroot}%{gem24_extbuilddir}
%__mv %{buildroot}%{gem_dir}/extensions/x86_64-linux/2.4.0/%{gem_name}-%{version}/* %{buildroot}%{gem24_extbuilddir}
fi
%{__perl} -MFile::Find -le '
    find ({ wanted => \&wanted, no_chdir => 1}, "%{buildroot}");
    for my $x (sort @dirs, @files) {
        push @ret, $x unless indirs($x);
    }
    print join "\n", sort @ret;
    sub wanted {
        return if /auto$/;
        local $_ = $File::Find::name;
        my $f = $_; s|^\Q%{buildroot}\E||;
        return unless length;
        return $files[@files] = $_ if -f $f;
        $d = $_;
        /\Q$d\E/ && return for reverse sort @INC;
        $d =~ /\Q$_\E/ && return
            for qw|/etc %_prefix/man %_prefix/bin %_prefix/share|;
        $dirs[@dirs] = $_;
      }

    sub indirs {
        my $x = shift;
        $x =~ /^\Q$_\E\// && $x ne $_ && return 1 for @dirs;
    }
' > $RPM_BUILD_DIR/%{filelist}
%__sed -i -e 's/.*/\"&\"/g' $RPM_BUILD_DIR/%{filelist}
find %{buildroot} -type f -exec %{__sed} -i -e 's|/usr/local/bin/ruby|/usr/bin/ruby%{ruby_ver}|g' {} \;

if [[ "%{name}" == *plugins* || "%{name}" == *metrics* || "%{name}" == *mutator* || "%{name}" == *handler* ]]; then
  if [ -d %{buildroot}%{_bindir} ]; then
    for file in `ls %{buildroot}%{_bindir}`
    do
      if [[ $file == metric* ]]; then
        if [ ! -d %{buildroot}%{metrics} ];then
            %__mkdir_p %{buildroot}%{metrics}
        fi
        %{__ln_s} -f %{_bindir}/$file %{buildroot}%{metrics}/$file
        echo "%{metrics}/$file" >> %{filelist}
      elif [[ $file == check* ]]; then
        if [ ! -d %{buildroot}%{plugins} ];then
            %__mkdir_p %{buildroot}%{plugins}
        fi
        %{__ln_s} -f %{_bindir}/$file %{buildroot}%{plugins}/$file
        echo "%{plugins}/$file" >> %{filelist}
      elif [[ $file == mutator* ]]; then
        if [ ! -d %{buildroot}%{mutators} ];then
            %__mkdir_p %{buildroot}%{mutators}
        fi
        %{__ln_s} -f %{_bindir}/$file %{buildroot}%{mutators}/$file
        echo "%{mutators}/$file" >> %{filelist}
      elif [[ $file == handle* ]]; then
        if [ ! -d %{buildroot}%{handlers} ];then
            %__mkdir_p %{buildroot}%{handlers}
        fi
        %{__ln_s} -f %{_bindir}/$file %{buildroot}%{handlers}/$file
        echo "%{handlers}/$file" >> %{filelist}
      else
        if [ ! -d %{buildroot}%{plugins} ];then
            %__mkdir_p %{buildroot}%{plugins}
        fi
        %{__ln_s} -f %{_bindir}/$file %{buildroot}%{plugins}/$file
        echo "%{plugins}/$file" >> %{filelist}
      fi
    done
  fi
fi
exit 0

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{filelist}" != "/" ] && %__rm -rf %{_builddir}/%{filelist}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files -f %{filelist}


## end file
