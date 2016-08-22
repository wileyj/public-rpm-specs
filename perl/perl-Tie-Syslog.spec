%define cpan_name Tie::Syslog
%define pkgname Tie-Syslog
%define cpan_version %(echo `curl -s https://metacpan.org/pod/%{cpan_name} | grep "Module version" | awk {'print $4'} |tr -d 'itemprop="softwareVersion"></span>'`)
%define filelist %{pkgname}-%{version}-filelist

name:      perl-Tie-Syslog
summary:   Tie-Syslog - Tie a filehandle to Syslog. If you Tie STDERR, then all STDERR errors are automatically caught, or you can debug by Carp'ing to STDERR, etc. (Good for CGI error logging.)
version: %{cpan_version}
release:   1.%{dist}
license:   Artistic
Vendor: %{vendor}
Packager: %{packager}
group:     Applications/CPAN
url:       http://www.cpan.org
buildroot: %{_tmppath}/%{name}-%{version}-%(id -u -n)
prefix:    %(echo %{_prefix})
BuildRequires: perl, perl-srpm-macros,  perl-devel, perl-libs, perl-ExtUtils-MakeMaker
%if 0%{?el6}
buildarch: x86_64
%else
buildarch: noarch
%endif
Provides: %{name}
%{?load: %{_sourcedir}/macros.perl}

%description
This module allows you to tie a filehandle (output only) to syslog. This
becomes useful in general when you want to capture any activity that
happens on STDERR and see that it is syslogged for later perusal. You
can also create an arbitrary filehandle, say LOG, and send stuff to syslog
by printing to this filehandle. This module depends on the Sys::Syslog
module to actually get info to syslog.

Tie your filehandle to syslog using a glob to the filehandle. When it is
tied to the 'Tie::Syslog' class, you may optionally pass four arguments
that determine the behavior of the output bound to syslog.

You first specify a facility and priority to direct your filehandle traffic
to the proper channels in syslog. I suggest reviewing a manpage for syslog
on your local system to identify what the facilities and priorities actually
are. Nonetheless, this first argument is specified as a string consisting
of the facility followed by a dot, followed by the priority. For example,
the default setting is 'local0.error'. (Note: I believe Linux uses 'err'
rather than 'error'.) If you do not specify a first arg, this default is
used.

The second argument is an identifier string. This is the string that shows
up in evey line of output that syslog writes. You may use this identifier
to help sort out syslog lines produced by different applications (with
different id's.) If you do not specify a value for this argument, it will
default to the name of the running program. (This is derived from the
special $0 variable, stripping off everything up to the final appearing
forward slash character.)

The third argument is a string of comma separated log options specific
to syslog. Current documentation supports 'pid,cons,ndelay,nowait'. Check
your local listings, as you may pass values that are only part of your
local system. I suggest checking your man pages for syslog, and perhaps
looking inside your site_perl/$archname/sys/syslog.ph for other such values.
If you do not pass this third argument, it defaults to the string 'pid',
which makes syslog put a [12345] pid value on each line of output.

The fourth argument is either the string 'inet' or 'unix'. This is
passed to the Sys::Syslog::setlogsock() call to specify the socket type
to be used when opening the connection to syslog. If this argument is
not specified, then the default used is 'inet'. Many perl installations
still have original Sys::Syslog which does not have the setlogsock()
routine. There is also no $VERSION constant to test in Sys::Syslog, so
we'll test the symbol table to see if the routine exists. If the routine
does not exist, then the fourth argument is silently ignored. I did not
want to require people to have "the latest" version of perl just to use
this module.


Note:  You can now optionally pass a reference to a Filehandle as the *very*
first arg (before the 'Tie::Syslog' even...)  The *only* time you'd do
this is if you are experiencing trouble using your tied filehandle with
other code that expects to do calls like fileno() and binmode() to
operate on this tied filehandle. The TIEHANDLE api gives us no way (that
I have found) to get access to the actual tied variable, or filehandle in
this case. So, I have resorted to just passing it in as a arg right up front
and just storing it in the object. **THERE ARE PROBLEMS WITH THIS!!!** Be
aware, those of you this may affect...


An aside on using 'STDERR':

The blessed object that is returned from tie also has one additional
member function. In the case that you tie the filehandle 'STDERR' (or
a dup'ed copy of STDERR) then you may want to capture information
going to the warn() and die() functions. You may call ExtendedSTDERR()
to setup the proper handler function to deal with the special signals
for __DIE__ and __WARN__. Because this module really has no knowledge
of what filehandle is being tied, I contemplated trying to make this
automatic for when the STDERR filehandle is used. But, alas, one may
have a different name for what is really STDERR, plus the TIEHANDLE
function has no way of knowing what the filehandle symbol is anyway.
I also decided to put the logic of how to handle the two signal cases
into this module, when perhaps they might be more suited to be at the
level of whoever is calling this module. Well, you don't have to call
the routine ExtendedSTDERR() if you don't like what it does. I felt
obligated to provide a proper solution to the signal handling since
a common use of this module would be to capture STDERR for syslogging.

  my $x = tie *STDERR, 'Tie::Syslog', 'local0.debug';
  $x->ExtendedSTDERR();            ## set __DIE__,__WARN__ handler

  print STDERR "I made an error."; ## this will be syslogged
  printf STDERR "Error %d", 42;    ## syslog as "Error 42"
  warn "Another error was made.";  ## this will also be syslogged
  eval {
      die "exception thrown";      ## this is *NOT* syslogged
  };
  die "Killing me softly?!";       ## syslogged, then script ends

  undef $x;                        ## be sure to do this, else warns!
  untie *STDERR;


When used with STDERR, combined with the good habit of using the perl "-w"
switch, this module happens to be useful in catching unexpected errors in
any of your code, or team's code. Tie::Syslog is pretty brain-dead. However,
it can become quite flexible if you investigate your options with the
actual syslog daemon. Syslog has a variety of options available, including
notifying console, logging to other machines running syslog, or email
support in the event of Bad Things. Consult your syslog documentation
to get /etc/syslog.conf setup by your sysadmin and use Tie::Syslog to get
information into those channels.

%prep
curl -o $RPM_SOURCE_DIR/%{name}.tar.gz `curl -s https://metacpan.org/pod/%{cpan_name} | grep "tar.gz" | cut -d '"' -f4`
tar -xzvf $RPM_SOURCE_DIR/%{name}.tar.gz
#%setup -q -n %{pkgname}-%{version} 
chmod -R u+w %{_builddir}/%{pkgname}-%{version}

%build
cd $RPM_BUILD_DIR/%{pkgname}-%{cpan_version}
grep -rsl '^#!.*perl' . |
grep -v '.bak$' |xargs --no-run-if-empty \
%__perl -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)'
CFLAGS="$RPM_OPT_FLAGS"
%{__perl} Makefile.PL `%{__perl} -MExtUtils::MakeMaker -e ' print qq|PREFIX=%{buildroot}%{_prefix}| if \$ExtUtils::MakeMaker::VERSION =~ /5\.9[1-6]|6\.0[0-5]/ '`
echo "Y" | %{__make} %{?_smp_mflags} OPTIMIZE="%{optflags}" 

%install
cd $RPM_BUILD_DIR/%{pkgname}-%{cpan_version}
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%{makeinstall} `%{__perl} -MExtUtils::MakeMaker -e ' print \$ExtUtils::MakeMaker::VERSION <= 6.05 ? qq|PREFIX=%{buildroot}%{_prefix}| : qq|DESTDIR=%{buildroot}| '`

cmd=/usr/share/spec-helper/compress_files
[ -x $cmd ] || cmd=/usr/lib/rpm/brp-compress
[ -x $cmd ] && $cmd

# SuSE Linux
if [ -e /etc/SuSE-release -o -e /etc/UnitedLinux-release ]
then
    %{__mkdir_p} %{buildroot}/var/adm/perl-modules
    %{__cat} `find %{buildroot} -name "perllocal.pod"`  \
        | %{__sed} -e s+%{buildroot}++g                 \
        > %{buildroot}/var/adm/perl-modules/%{name}
fi

# remove special files
find %{buildroot} -name "perllocal.pod" \
    -o -name ".packlist"                \
    -o -name "*.bs"                     \
    |xargs -i rm -f {}

# no empty directories
find %{buildroot}%{_prefix}             \
    -type d -depth                      \
    -exec rmdir {} \; 2>/dev/null

%{__perl} -MFile::Find -le '
    find({ wanted => \&wanted, no_chdir => 1}, "%{buildroot}");
    #print "%doc  src Changes examples README";
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
    ' > %filelist

[ -z %filelist ] && {
    echo "ERROR: empty %files listing"
    exit -1
    }

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
[ "%{_builddir}/%{srcname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{srcname}-%{version}
[ "%{_builddir}/%{pkgname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{pkgname}-%{version}

%files -f %{pkgname}-%{cpan_version}/%filelist
%defattr(-,root,root)

%changelog