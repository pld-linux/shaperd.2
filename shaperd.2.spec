Summary:	Shaperd (CBQ) - bandwidth limiting
Summary(pl):	Shaperd (CBQ) - dzielenie ³±cza
Name:		shaperd.2
Version:	200beta61
Release:	1
License:	GPL
Group:		Networking/Admin
#Source0:	http://sp9wun.republika.pl/prg/%{name}.%{version}.tar.gz
# Changed source to decrease traffic at republika.pl
Source0:	http://www.cbq.trzepak.net/prg/%{name}.%{version}.tar.gz
Source1:        %{name}.init
#URL:		http://sp9wun.republika.pl/linux/shaperd_cbq.html
URL:		http://www.cbq.trzepak.net/linux/shaperd_cbq.html
PreReq:		rc-scripts
Requires(post,preun): /sbin/chkconfig
Requires:	firewall-userspace-tool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This program limits bandwidth on the ethernet/ppp interface and
divides it between the hosts in the local network.

%description -l pl
Program potrafi ograniczaæ przepustowo¶æ interfejsu ethernet/ppp oraz
dzieliæ dostêpne pasmo pomiêdzy komputery w sieci lokalnej.

%prep
%setup -q -n %{name}

%build
%{__cc} %{rpmcflags} usr/src/shaperd/shaperd.c -o usr/src/shaperd/shaperd

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/{cron.hourly,shaper},%{_initrddir},/var/lib/shaper}

install ./usr/src/shaperd/shaperd $RPM_BUILD_ROOT%{_sbindir}
install ./etc/shaper/* $RPM_BUILD_ROOT%{_sysconfdir}/shaper
install ./etc/cron.hourly/ckwintalk $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly
install ./var/www/kto.php $RPM_BUILD_ROOT/var/lib/shaper
install %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/shaperd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add shaperd
if [ -f /var/lock/subsys/shaperd ]; then
	/etc/rc.d/init.d/shaperd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/shaperd start\" to start shaperd daemon." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/shaperd ]; then
		/etc/rc.d/init.d/shaperd stop >&2
	fi
	/sbin/chkconfig --del shaperd
fi

%files
%defattr(644,root,root,755)
%doc COPYING
%attr(640,root,root) %verify(not size md5 mtime) %config(noreplace) %{_sysconfdir}/shaper/*
%attr(755,root,root) %{_sbindir}/shaperd
%attr(754,root,root) %{_initrddir}/shaperd
%attr(750,root,root) %{_sysconfdir}/cron.hourly/ckwintalk
%dir /var/lib/shaper
/var/lib/shaper/kto.php
