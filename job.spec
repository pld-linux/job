# TODO
# - optflags
Summary:	Linux Jobs
Summary(pl.UTF-8):	Narzędzia do obsługi zadań pod Linuksem
Name:		job
Version:	1.5.0
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	ftp://oss.sgi.com/projects/pagg/download/%{name}-%{version}.tar.gz
# Source0-md5:	4cc7c983765c934e33d4078bf530a978
URL:		http://oss.sgi.com/projects/pagg/
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The job package provides a set of commands, a PAM module, man pages,
and configuration files. The commands are used to send signals to
jobs, wait on jobs, get status information about jobs, and for
administrators to control process attachment to jobs. The PAM module
allows the administrator to specify which point-of-entry services on
the system (rlogin, gdm, xdm, ftp, etc.) should create new jobs.

%description -l pl.UTF-8
Pakiet job dostarcza zestaw poleceń, moduł PAM, strony podręcznika
oraz plik konfiguracyjny. Polecenia służą do wysyłania sygnałów do
zadań, oczekiwania na zadania, odczytu informacji o zadaniach oraz dla
administratorów do kontroli dołączania procesów do zadań. Moduł PAM
umożliwia administratorowi określenie, które usługi wejściowe systemu
(rlogin, gdm, xdm, ftp itp.) powinny tworzyć nowe zadania.

%prep
%setup -q -n %{name}

%build
# TODO: optflags
%{__make} build \
	ROOT="$RPM_BUILD_ROOT"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	ROOT="$RPM_BUILD_ROOT"

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ "$1" = 0 ] ; then
	SAFE=`fgrep -s pam_job.so /etc/pam.d/* | wc -l`
	if [ $SAFE -ne 0 ] ; then
		echo "You must remove all references to pam_job.so in the "
		echo "/etc/pam.d/* config files before attempting to uninstall"
		echo "the job package."
		echo ""
		exit 1
	fi
	/sbin/chkconfig --del job
fi
exit 0

%post
/sbin/chkconfig --add job
echo "You must add references to pam_job.so in the /etc/pam.d/* config"
echo "files to enable the PAM services for creating jobs.  You only"
echo "need to add the reference for services that you want to fall under"
echo "job control."
echo ""
echo "Example entry when able to use session modules:"
echo ""
echo "    session    optional    /lib/security/pam_job.so"
echo ""
echo "Example entry when required to use account modules:"
echo ""
echo "    account    optional   /lib/security/pam_job.so"
echo ""
echo "Consult the %{_docdir}/job-1.4/README file for additional"
echo "information about the PAM module."
echo ""
exit 0

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING INSTALL README
%attr(755,root,root) %{_bindir}/jdetach
%attr(755,root,root) %{_bindir}/jkill
%attr(755,root,root) %{_bindir}/jsethid
%attr(755,root,root) %{_bindir}/jstat
%attr(755,root,root) %{_bindir}/jwait
%attr(755,root,root) %{_bindir}/jattach
%attr(755,root,root) %{_libdir}/libjob.so
%attr(755,root,root) /%{_lib}/security/pam_job.so
%attr(754,root,root) /etc/rc.d/init.d/job
%{_mandir}/*/*
# -devel?
#%{_includedir}/job.h
