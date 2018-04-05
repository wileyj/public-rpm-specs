AutoReqProv: no
%global alinux_ruby 24
%global ruby_ver 2.4
%global gem_dir %{gem24_dir}



%define filelist %{name}-%{version}-filelist
%global sensu_base %{_sysconfdir}/sensu
%global plugins    %{sensu_base}/plugins
%global metrics    %{sensu_base}/metrics
%global handlers   %{sensu_base}/handlers
%global extensions %{sensu_base}/extensions
%global mutators   %{sensu_base}/mutators

%global gem_name right_aws
Name: rubygem%{alinux_ruby}-right_aws
Version: 3.1.0
Release: 1.%{dist}
AutoReqProv : no
Summary: rubygem right_aws
Group: Development/Languages
License: GPL
URL: None
Vendor: %{vendor}
Packager: %{packager}
Requires: ruby%{alinux_ruby} rubygems%{alinux_ruby}
Provides: rubygem%{alinux_ruby}-right_aws = %{version}
Provides: rubygem%{alinux_ruby}(right_aws) = %{version}
Obsoletes: rubygem%{alinux_ruby}-right_aws < %{version}
Obsoletes: rubygem%{alinux_ruby}(right_aws) < %{version}


Requires: rubygem%{alinux_ruby}-right_http_connection  >= 1.2.5


%description
== DESCRIPTION:

The RightScale AWS gems have been designed to provide a robust, fast, and secure interface to Amazon EC2, EBS, S3, SQS, SDB, and CloudFront.
These gems have been used in production by RightScale since late 2006 and are being maintained to track enhancements made by Amazon.
The RightScale AWS gems comprise:

- RightAws::Ec2 -- interface to Amazon EC2 (Elastic Compute Cloud) and the
  associated EBS (Elastic Block Store)
- RightAws::S3 and RightAws::S3Interface -- interface to Amazon S3 (Simple Storage Service)
- RightAws::Sqs and RightAws::SqsInterface -- interface to first-generation Amazon SQS (Simple Queue Service) (API version 2007-05-01)
- RightAws::SqsGen2 and RightAws::SqsGen2Interface -- interface to second-generation Amazon SQS (Simple Queue Service) (API version 2008-01-01)
- RightAws::SdbInterface and RightAws::ActiveSdb -- interface to Amazon SDB (SimpleDB)
- RightAws::AcfInterface -- interface to Amazon CloudFront, a content distribution service

== FEATURES:

- Full programmmatic access to EC2, EBS, S3, SQS, SDB, and CloudFront.
- Complete error handling: all operations check for errors and report complete
  error information by raising an AwsError.
- Persistent HTTP connections with robust network-level retry layer using
  RightHttpConnection).  This includes socket timeouts and retries.
- Robust HTTP-level retry layer.  Certain (user-adjustable) HTTP errors returned
  by Amazon's services are classified as temporary errors.
  These errors are automaticallly retried using exponentially increasing intervals.
  The number of retries is user-configurable.
- Fast REXML-based parsing of responses (as fast as a pure Ruby solution allows).
- Uses libxml (if available) for faster response parsing.
- Support for large S3 list operations.  Buckets and key subfolders containing
  many (> 1000) keys are listed in entirety.  Operations based on list (like
  bucket clear) work on arbitrary numbers of keys.
- Support for streaming GETs from S3, and streaming PUTs to S3 if the data source is a file.
- Support for single-threaded usage, multithreaded usage, as well as usage with multiple
  AWS accounts.
- Support for both first- and second-generation SQS (API versions 2007-05-01
  and 2008-01-01).  These versions of SQS are not compatible.
- Support for signature versions 0 and 1 on SQS, SDB, and EC2.
- Interoperability with any cloud running Eucalyptus (http://eucalyptus.cs.ucsb.edu)
- Test suite (requires AWS account to do "live" testing).

%prep
%build
%install
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install --install-dir %{buildroot}/%{gem_dir} --bindir %{buildroot}/%{_bindir} --no-rdoc --no-ri --no-doc --ignore-dependencies %{gem_name} -v %{version}
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
