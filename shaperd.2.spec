Summary:	Shaperd - bandwidth limiting
Summary(pl):	Shaperd - dzielenie ³±cza
Name:		shaperd.2
Version:	2.24
Release:	0.9
License:	GPL
Group:		Networking/Admin
#Source0:	http://sp9wun.republika.pl/prg/%{name}.%{version}.tar.gz
# Changed source to decrease traffic at republika.pl
Source0:	http://www.cbq.trzepak.net/prg/%{name}.%{version}.tar.gz
# Source0-md5:	e6e7a91c5c08e2dbcf8c48fa54bff559
Source1:	%{name}.init
Source2:	%{name}.conf
Patch0:		%{name}-fhs.patch
Patch1:		%{name}-iptables_path.patch
#URL:		http://sp9wun.republika.pl/linux/shaperd_cbq.html
URL:		http://www.cbq.trzepak.net/linux/shaperd_cbq.html
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	firewall-userspace-tool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_phpdir		%{_datadir}/%{name}
%define		_sysconfdir	/etc/%{name}
%define		_apache1dir	/etc/apache
%define		_apache2dir	/etc/httpd

%description
This program limits bandwidth on the ethernet/ppp interface and
divides it between the hosts in the local network.

%description -l pl
Program potrafi ograniczaæ przepustowo¶æ interfejsu ethernet/ppp oraz
dzieliæ dostêpne pasmo pomiêdzy komputery w sieci lokalnej.

%package php
Summary:	PHP script for shaperd
Summary(pl):	Skrypt PHP dla shaperd
Group:		Networking/Admin
Requires:	%{name} = %{version}
Requires:	php
Requires:	webserver

%description php
PHP script for shaperd.

%description php -l pl
Skrypt PHP dla shaperd.

%prep
%setup -q -n shaperd
%patch0 -p1
%patch1 -p1

%build
%{__make} clean
# this file has its own rule in Makefile, without CFLAGS...
%{__cc} %{rpmcflags} -c shaperd_old.c
%{__make} \
	CC=%{__cc} \
	CFLAGS="%{rpmcflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir},%{_initrddir},/var/lib/shaper,%{_phpdir},/etc/httpd}

install shaperd $RPM_BUILD_ROOT%{_sbindir}
install etc/shaper/* $RPM_BUILD_ROOT%{_sysconfdir}
install var/www/html/kto.php $RPM_BUILD_ROOT%{_phpdir}/shaperd.php
install %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/shaperd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add shaperd
if [ -f /var/lock/subsys/shaperd ]; then
	/etc/rc.d/init.d/shaperd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/shaperd start\" to start shaperd daemon." >&2
fi

# apache1
if [ -d %{_apache1dir}/conf.d ]; then
        ln -sf %{_sysconfdir}/apache-%{name}.conf %{_apache1dir}/conf.d/99_%{name}.conf
        if [ -f /var/lock/subsys/apache ]; then
                /etc/rc.d/init.d/apache restart 1>&2
        fi
fi
# apache2
if [ -d %{_apache2dir}/httpd.conf ]; then
        ln -sf %{_sysconfdir}/apache-%{name}.conf %{_apache2dir}/httpd.conf/99_%{name}.conf
        if [ -f /var/lock/subsys/httpd ]; then
                /etc/rc.d/init.d/httpd restart 1>&2
        fi
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/shaperd ]; then
		/etc/rc.d/init.d/shaperd stop >&2
	fi
	/sbin/chkconfig --del shaperd
fi
if [ "$1" = "0" ]; then
        # apache1
        if [ -d %{_apache1dir}/conf.d ]; then
                rm -f %{_apache1dir}/conf.d/99_%{name}.conf
                if [ -f /var/lock/subsys/apache ]; then
                        /etc/rc.d/init.d/apache restart 1>&2
                fi
        fi
        # apache2
        if [ -d %{_apache2dir}/httpd.conf ]; then
                rm -f %{_apache2dir}/httpd.conf/99_%{name}.conf
                if [ -f /var/lock/subsys/httpd ]; then
                        /etc/rc.d/init.d/httpd restart 1>&2
                fi
        fi
fi

%files
%defattr(644,root,root,755)
%doc kto-daemon usr/share/docs/shaperd-2.%{version}/shaperd_cbq.html
%doc usr/share/docs/shaperd-2.%{version}/shaperd_cbq_en.html
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
%attr(755,root,root) %{_sbindir}/shaperd
%attr(754,root,root) %{_initrddir}/shaperd
%dir /var/lib/shaper

%files php
%defattr(644,root,root,755)
%attr(644,root,root) %{_phpdir}/shaperd.php
