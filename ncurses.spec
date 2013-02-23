%define date		20130202
%define	major		5
%define	majorminor	5.9
%define utf8libname	%mklibname %{name}w %{major}
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname -d %{name}
%define utf8devname	%mklibname -d %{name}w

%bcond_without	uclibc

# ugly as fuck, but at least mostly harmless to children and animals..
%define libgen()\
%package -n	%2%{_lib}%{1}%{major}\
Summary:	Ncurses %{1} library\
Group:		System/Libraries\
Conflicts:	%{_lib}ncurses%{major} < 5.9-6.20120922.1 \
Conflicts:	%{_lib}ncursesw%{major} < 5.9-6.20120922.1 \
\
%description -n	%2%{_lib}%{1}%{major}\
This package comes with lib%{1} from the ncurses library.\
\
%files -n	%2%{_lib}%{1}%{major}\
%{3}%{_libdir}/lib%{1}.so.%{major}*\
%{nil}

Summary:	A CRT screen handling and optimization package
Name:		ncurses
Version:	5.9
Release:	6.%{date}.2
License:	MIT
Group:		System/Libraries
Url:		http://www.gnu.org/software/ncurses/ncurses.html
Source0:	ftp://invisible-island.net/ncurses/current/%{name}-%{version}-%{date}.tgz
Source4:	ncurses-resetall.sh
Source5:	ncurses-useful-terms
Patch1:		ncurses-5.6-xterm-debian.patch
# Alias "console" to "linux"
Patch2:		ncurses-5.9-20120811-linux-console.patch
Patch7:		ncurses-5.9-urxvt.patch
Patch8:		ncurses-5.9-20121208-config-dont-print-standard-lib64-path.patch
BuildRequires:	gpm-devel
BuildRequires:	sharutils
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-15
%endif
Conflicts:	%{name}-extraterms < 5.9-6.20121026.3

%description
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

%package -n	uclibc-%{name}
Summary:	Tools for ncurses built against uClibc
Group:		System/Libraries

%description -n	uclibc-%{name}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.


# to be killed
###############################################################################
%package -n	%{libname}
Summary:	The development files for applications which use ncurses
Group:		System/Libraries

%description -n	%{libname}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.


%libgen form %{nil} %{nil} %{nil}
%libgen menu %{nil} %{nil} %{nil}
%libgen panel %{nil} %{nil} %{nil}

%libgen formw %{nil} %{nil} %{nil}
%libgen menuw %{nil} %{nil} %{nil}
%libgen panelw %{nil} %{nil} %{nil}

%if %{with uclibc}
%libgen formw uclibc- %{uclibc_root}
%libgen menuw uclibc- %{uclibc_root}
%libgen panelw uclibc- %{uclibc_root}
%libgen tic uclibc- %{uclibc_root}
%libgen tinfo uclibc- %{uclibc_root}
%endif

%package -n	%{utf8libname}
Summary:	Ncurses libraries which support UTF8
Group:		System/Libraries

%description -n %{utf8libname}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

This package contains ncurses libraries which support wide char (UTF8),
and is not compatible with those without.

%package -n	uclibc-%{utf8libname}
Summary:	Ncurses libraries which support UTF8 (uClibc linked)
Group:		System/Libraries

%description -n uclibc-%{utf8libname}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

This package contains ncurses libraries which support wide char (UTF8),

%package	extraterms
Summary:	Some exotic terminal descriptions
Group:		System/Libraries
BuildArch:	noarch

%description	extraterms
Install the ncurses-extraterms package if you use some exotic terminals.

%package -n	%{devname}
Summary:	The development files for applications which use ncurses
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
# just keep this depdenency for untangling initial dependency issues..
%if "%{_lib}" == "lib64"
Provides:	devel(libncurses(64bit)) 
%else
Provides:	devel(libncurses) 
%endif
Provides:	pkgconfig(ncurses)
Provides:	ncursesw-devel = %{version}-%{release}
Requires:	%{utf8libname} = %{version}
Requires:	%{_lib}formw%{major} = %{version}
Requires:	%{_lib}menuw%{major} = %{version}
Requires:	%{_lib}panelw%{major} = %{version}
%if %{with uclibc}
Requires:	uclibc-%{utf8libname} = %{version}
Requires:	uclibc-%{_lib}tic%{major} = %{version}
Requires:	uclibc-%{_lib}tinfo%{major} = %{version}
Requires:	uclibc-%{_lib}formw%{major} = %{version}
Requires:	uclibc-%{_lib}menuw%{major} = %{version}
Requires:	uclibc-%{_lib}panelw%{major} = %{version}
# /usr/include/termcap.h conflicts
Conflicts:	termcap-devel > 2.0.8-53

%endif
Obsoletes:	%mklibname -d %name 5
Obsoletes:	%mklibname -d %{name}w 5
Conflicts:	%{_lib}ncurses-devel < 5.7-3.20091128.2
%rename		%{utf8devname}

%description -n	%{devname}
The header files and libraries for developing applications that use
the ncurses CRT screen handling and optimization package.

Install the ncurses-devel package if you want to develop applications
which will use ncurses.

%package -n	termcap
Summary:	The terminal feature database used by certain applications
Group:		System/Libraries
Epoch:		1
BuildArch:	noarch

%description -n	termcap
The termcap package provides the /etc/termcap file.  /etc/termcap is
a database which defines the capabilities of various terminals and
terminal emulators.  Certain programs use the /etc/termcap file to
access various features of terminals (the bell, colors, and graphics,
etc.).

%prep
%setup -q -n %{name}-%{version}-%{date}

%patch7 -p1 -b .urxvt~

# regenerating configure needs patched autoconf, so modify configure
# directly
%patch1 -p1 -b .deb~

%patch2 -p1 -b .console~
%patch8 -p1 -b .lib64~

find . -name "*.orig" -o -name "*~" | xargs rm -f
# fix some permissions
chmod 755 c++/edit_cfg.sh test/listused.sh test/configure test/tracemunch

# we don't need nor want this, and it also pulls in a dependency on /usr/bin/make
rm -rf test/package

%build
export PKG_CONFIG_LIBDIR=%{_libdir}/pkgconfig

CONFIGURE_TOP="$PWD"

%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure \
	--includedir=%{uclibc_root}%{_includedir} \
	--without-libtool \
	--with-shared \
	--without-normal \
	--with-cxx \
	--enable-overwrite \
	--without-profile \
	--with-gpm \
	--disable-termcap \
	--disable-getcap \
	--enable-const \
	--enable-hard-tabs \
	--enable-hash-map \
	--enable-no-padding \
	--enable-sigwinch \
	--without-ada \
	--enable-widec \
	--enable-xmc-glitch \
	--enable-colorfgbg \
	--disable-pc-files \
	--with-ospeed=unsigned \
	--without-develop \
	--without-cxx-binding \
	--without-tests \
	--with-termlib=tinfo \
	--with-ticlib=tic \
	--disable-tic-depends

%make
popd
%endif


# tODO: this should die
mkdir -p ncurses-normal
pushd ncurses-normal
%configure2_5x \
	--without-libtool \
	--with-shared \
	--with-normal \
	--with-cxx \
	--without-debug \
	--enable-overwrite \
	--without-profile \
	--with-gpm \
	--enable-termcap \
	--enable-getcap \
	--enable-const \
	--enable-hard-tabs \
	--enable-hash-map \
	--enable-no-padding \
	--enable-sigwinch \
	--without-ada \
	--disable-widec \
	--enable-xmc-glitch \
	--enable-colorfgbg \
	--disable-pc-files \
	--with-ospeed=unsigned \
	--without-progs

%make
popd

mkdir -p ncurses-utf8
pushd ncurses-utf8
%configure2_5x \
	--with-pkg-config-libdir=%{_libdir}/pkgconfig \
	--without-libtool \
	--with-shared \
	--with-normal \
	--with-cxx \
	--without-debug \
	--enable-overwrite \
	--without-profile \
	--with-gpm \
	--enable-termcap \
	--enable-getcap \
	--enable-const \
	--enable-hard-tabs \
	--enable-hash-map \
	--enable-no-padding \
	--enable-sigwinch \
	--without-ada \
	--enable-widec \
	--enable-xmc-glitch \
	--enable-colorfgbg \
	--enable-pc-files \
	--with-ospeed=unsigned

%make
popd

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
install -d %{buildroot}%{uclibc_root}/%{_lib}
mv %{buildroot}%{uclibc_root}%{_libdir}/libncursesw.so.* %{buildroot}%{uclibc_root}/%{_lib}
rm %{buildroot}%{uclibc_root}%{_libdir}/libncursesw.so
#ln -sr %{buildroot}%{uclibc_root}/%{_lib}/libncursesw.so.%{majorminor} %{buildroot}%{uclibc_root}%{_libdir}/libncursesw.so
cat > %{buildroot}%{uclibc_root}%{_libdir}/libncursesw.so << EOF
/* GNU ld script
Just linking against all ncurses libraries as needed...
*/
`%__cc -fuse-ld=bfd    -Wl,--verbose 2>&1 | sed -n '/OUTPUT_FORMAT/,/)/p'`
GROUP ( AS_NEEDED ( %{uclibc_root}/%{_lib}/libncursesw.so.%{majorminor} %{uclibc_root}%{_libdir}/libtinfo.so.%{majorminor} %{uclibc_root}%{_libdir}/libtic.so.%{majorminor}) )
EOF

rm  %{buildroot}%{uclibc_root}%{_libdir}/*.a
%endif

# we only install the libraries for a while untill all our packages has been
# rebuilt against the unicode version and no packages needs this anymore
pushd ncurses-normal
make install.libs DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/lib*.{a,so}
popd

pushd ncurses-utf8
%makeinstall_std
popd

# the resetall script
install -m 755 %{SOURCE4} %{buildroot}%{_bindir}/resetall
# we don't want this in doc
rm -f c++/demo

mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libncurses{,w}.so.* %{buildroot}/%{_lib}
rm %{buildroot}%{_libdir}/libncursesw.so
ln -sr %{buildroot}/%{_lib}/libncursesw.so.%{majorminor} %{buildroot}%{_libdir}/libncursesw.so
for i in form menu ncurses panel; do
	ln -s lib${i}w.a %{buildroot}%{_libdir}/lib${i}.a
	ln -s lib${i}w.so %{buildroot}%{_libdir}/lib${i}.so
done
ln -s libncursesw.so %{buildroot}%{_libdir}/libcurses.so
ln -s libncursesw.a %{buildroot}%{_libdir}/libcurses.a
ln -s libncurses++w.a %{buildroot}%{_libdir}/libncurses++.a

#
# FIXME
# OK do not time to debug it now
#
cp %{buildroot}%{_datadir}/terminfo/x/xterm %{buildroot}%{_datadir}/terminfo/x/xterm2
cp %{buildroot}%{_datadir}/terminfo/x/xterm-new %{buildroot}%{_datadir}/terminfo/x/xterm

#
# remove unneeded/unwanted files
# have to be done before find commands below
#
rm -f %{buildroot}%{_libdir}/terminfo

# fwang: avoid conflict with kon package
rm -f %{buildroot}%{_datadir}/terminfo/k/kon

# bero: Build termcap from the terminfo database
mkdir -p %{buildroot}%_sysconfdir
%if ! %cross_compiling
LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_lib}:$RPM_BUILD_ROOT%{_libdir}:$LD_LIBRARY_PATH $RPM_BUILD_ROOT%{_bindir}/tic -Ct misc/terminfo.src > %{buildroot}%{_sysconfdir}/termcap
%else
tic -Ct misc/terminfo.src > %{buildroot}%{_sysconfdir}/termcap
%endif

#
# FIXME
#
(cd %{buildroot} ; find usr/share/terminfo      -type d | perl -pe 's||%%dir /|') > %{name}.list
(cd %{buildroot} ; find usr/share/terminfo -not -type d | perl -pe 's||/|')       > %{name}-extraterms.list
perl -pe 's||%{_datadir}/terminfo/|' %{SOURCE5} >> %{name}.list

perl -ni -e 'BEGIN { open F, "%{name}.list"; /^%/ or $s{$_} = 1 foreach <F>; } print unless $s{$_}' %{name}-extraterms.list

find %{buildroot}/%{_libdir} -name 'lib*.a' -not -type d -not -name "*_g.a" -not -name "*_p.a" -not -name "*w.a" | sed -e "s#^%{buildroot}##" > %{libname}-devel.list

# can't replace directory with symlink (rpm bug), symlink all headers
mkdir $RPM_BUILD_ROOT%{_includedir}/ncurses{,w}
for l in $RPM_BUILD_ROOT%{_includedir}/*.h; do
    ln -sr $l $RPM_BUILD_ROOT%{_includedir}/ncurses
    ln -sr $l $RPM_BUILD_ROOT%{_includedir}/ncursesw
done

%multiarch_includes %{buildroot}%{_includedir}/curses.h

%files -f %{name}.list
%doc README ANNOUNCE
%{_datadir}/tabset
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}%{_bindir}/*
%endif

%files -n %{libname}
%attr(755,root,root) /%{_lib}/libncurses.so.%{major}*

%files -n %{utf8libname}
%attr(755,root,root) /%{_lib}/libncursesw.so.%{major}*
# I have no clue on how nor where this actually gets created?!?!
%attr(755,root,root) %{_libdir}/libncursesw.so.%{major}

%if %{with uclibc}
%files -n uclibc-%{utf8libname}
%attr(755,root,root) %{uclibc_root}/%{_lib}/libncursesw.so.%{major}*
%endif

%files extraterms -f %{name}-extraterms.list
%doc README

%files -n %{devname}
%doc doc c++ test
%{_libdir}/libcurses.a
%{_libdir}/libcurses.so
%{_libdir}/libform.a
%{_libdir}/libform.so
%{_libdir}/libformw.a
%{_libdir}/libformw.so
%{_libdir}/libmenu.a
%{_libdir}/libmenu.so
%{_libdir}/libmenuw.a
%{_libdir}/libmenuw.so
%{_libdir}/libncurses++.a
%{_libdir}/libncurses++w.a
%{_libdir}/libncurses.a
%{_libdir}/libncurses.so
%{_libdir}/libncursesw.a
%{_libdir}/libncursesw.so
%{_libdir}/libpanel.a
%{_libdir}/libpanel.so
%{_libdir}/libpanelw.a
%{_libdir}/libpanelw.so
%{_libdir}/pkgconfig/formw.pc
%{_libdir}/pkgconfig/menuw.pc
%{_libdir}/pkgconfig/ncurses++w.pc
%{_libdir}/pkgconfig/ncursesw.pc
%{_libdir}/pkgconfig/panelw.pc
%{_includedir}/*.h
%{multiarch_includedir}/curses.h
%dir %{_includedir}/ncurses
%{_includedir}/ncurses/*.h
%dir %{_includedir}/ncursesw
%{_includedir}/ncursesw/*.h
%{_mandir}/man3/*
%if %{with uclibc}
%{uclibc_root}%{_libdir}/lib*.so
# not final, but just work around library issues for now..
%{uclibc_root}%{_includedir}/*
%endif

%files -n termcap
%{_sysconfdir}/termcap

%changelog
* Sun Jan  6 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.9-6.20121208.3
- drop dependency in library packages on 'ncurses' package as it's now being
  pulled in by 'basesystem-minimal' package in stead, thus eliminating a
  dependency loop

* Fri Dec 21 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.9-6.20121208.2
- fix libncursesw.so linker script

* Wed Oct 31 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.9-6.20121208.1
- new version

* Wed Oct 31 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.9-6.20121026.3
+ Revision: 821465
- enable gpm support for uclibc build
- include screen-256color in standard package
- move some terminfos to ncurses-extraterms package
- add xterm-256color as terminfo to include in main package
- update ancient path /usr/X11R6/bin/resize to /usr/bin/resize
- make ncurses-exterms noarch

* Mon Oct 29 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.9-6.20121026.2
+ Revision: 820512
- drop pkgconfig files again, just leave a manually added pkgconfig(ncurses) in
  stead to make package maintainers' lifes a bit easier for now..
- add output format to linker script so ldconfig won't complain

* Sun Oct 28 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.9-6.20121026.1
+ Revision: 820113
- new version
- add back pkgconfig files for ascii build for compatibility

* Sun Oct 28 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.9-6.20120922.5
+ Revision: 820079
- rebuild for pkgconfig() provides that got lost somehow earlier..
- add release to ncurses-devel provide

* Wed Oct 03 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.9-6.20120922.4
+ Revision: 818341
- add missing dependencies on uclibc library packages for devel package
- add compatibility directory & symlinks for headers

* Wed Oct 03 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.9-6.20120922.3
+ Revision: 818306
- create a linker script so that we're sure to automatically pick up and link
  against the necessary libraries for uclibc build

* Thu Sep 27 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.9-6.20120922.2
+ Revision: 817693
- add compatibility symlink to make apps trying to link with -lncurses to use
  libncursesw in stead
- drop release from versioned dependencies
- enable build of separate smaller libraries for uclibc build
- split individual libraries into separate packages
- fix packaging to only allow for building against unicode version of library,
  preparing for removal of non-utf8 build
- build uclibc linked version of binaries as well
- do uclibc build
- update to latest release

* Fri Aug 17 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.9-6.20120811.1
+ Revision: 815283
- reenable parallel build
- cleanups
- new snapshot
- just get tarball of latest snapshot rather than applying tons of patches
- add snapshot date to release tag

* Fri Mar 23 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.9-5
+ Revision: 786426
- get rid of test/packaging directory which one of the files of pulled in a
  dependency on /usr/bin/make

* Wed Mar 07 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.9-4
+ Revision: 782565
- cleanup a bit
- do no explicitly provide libfoo-devel

* Mon Jan 09 2012 Bernhard Rosenkraenzer <bero@bero.eu> 5.9-3
+ Revision: 759167
- Add current patches from upstream, adapt our patches
- Alias console to linux instead of symlinking the terminfo directories.
  (This gets the correct description into termcap as well)
- Build termcap package from terminfo sources
- Add konsole and konsole-256color to useful-terms
- Fix spelling errors

* Mon May 02 2011 Funda Wang <fwang@mandriva.org> 5.9-2
+ Revision: 662184
- fix multiarch usage
- update multiarch usage

  + Oden Eriksson <oeriksson@mandriva.com>
    - multiarch fixes

* Tue Apr 05 2011 Funda Wang <fwang@mandriva.org> 5.9-1
+ Revision: 650584
- update fie list
- new version 5.9

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 5.8-1
+ Revision: 640176
- New version 5.8

* Sun Jan 09 2011 Funda Wang <fwang@mandriva.org> 5.7-5.20110108.1mdv2011.0
+ Revision: 630740
- new patch series

* Wed Dec 01 2010 Funda Wang <fwang@mandriva.org> 5.7-5.20100925.1mdv2011.0
+ Revision: 604235
- update file list

  + Rémy Clouard <shikamaru@mandriva.org>
    - update rxvt-unicode terminfo definition

* Thu Sep 30 2010 Funda Wang <fwang@mandriva.org> 5.7-4.20100925.1mdv2011.0
+ Revision: 582124
- New patch series

* Fri Aug 06 2010 Funda Wang <fwang@mandriva.org> 5.7-4.20100731.1mdv2011.0
+ Revision: 566670
- New patches updated to 20100731

* Fri Apr 30 2010 Funda Wang <fwang@mandriva.org> 5.7-4.20091227.1mdv2010.1
+ Revision: 541252
- revert previous commit for version unfreeze

* Fri Apr 30 2010 Funda Wang <fwang@mandriva.org> 5.7-3.20100424.1mdv2010.1
+ Revision: 541215
- new rollpatch

* Thu Apr 08 2010 Rémy Clouard <shikamaru@mandriva.org> 5.7-3.20091227.2mdv2010.1
+ Revision: 533105
- add terminfo for rxvt-unicode (fix #42231)
- add rxvt-unicode to the list of useful terms so that it does not go into
  the extraterms subpackage

* Mon Dec 28 2009 Christophe Fergeau <cfergeau@mandriva.com> 5.7-3.20091227.1mdv2010.1
+ Revision: 483040
- update to latest patchset, fixes bug #56272

  + Pascal Terjan <pterjan@mandriva.org>
    - update patch series to 20091226

* Tue Dec 01 2009 Anssi Hannula <anssi@mandriva.org> 5.7-3.20091128.3mdv2010.1
+ Revision: 472448
- fix typo in conflicts (fixes #56135, noticed by Charles A Edwards)

* Mon Nov 30 2009 Funda Wang <fwang@mandriva.org> 5.7-3.20091128.2mdv2010.1
+ Revision: 471617
- move ncursesw.pc into w-devel

* Mon Nov 30 2009 Funda Wang <fwang@mandriva.org> 5.7-3.20091128.1mdv2010.1
+ Revision: 471609
- New patch series

* Sun Nov 29 2009 Guillaume Rousse <guillomovitch@mandriva.org> 5.7-3.20090516.2mdv2010.1
+ Revision: 471556
- enable pkgconfig support

* Sun May 17 2009 Funda Wang <fwang@mandriva.org> 5.7-3.20090516.1mdv2010.0
+ Revision: 376533
- New patch series

* Tue Feb 10 2009 Funda Wang <fwang@mandriva.org> 5.7-3.20090207.1mdv2009.1
+ Revision: 339223
- update upstream patches

* Tue Jan 13 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 5.7-3mdv2009.1
+ Revision: 329216
- spec file clean

* Sun Dec 21 2008 Oden Eriksson <oeriksson@mandriva.com> 5.7-2mdv2009.1
+ Revision: 317120
- rediffed one fuzzy patch
- fix build with -Werror=format-security (P6)

* Mon Nov 03 2008 Funda Wang <fwang@mandriva.org> 5.7-1mdv2009.1
+ Revision: 299340
- New version 5.7
- drop those old patches

* Thu Oct 23 2008 Götz Waschk <waschk@mandriva.org> 5.6-1.20080927.2mdv2009.1
+ Revision: 296698
- multiarch fix

* Sun Oct 12 2008 Funda Wang <fwang@mandriva.org> 5.6-1.20080927.1mdv2009.1
+ Revision: 292653
- Updated patch series to 20080927

* Tue Aug 26 2008 Funda Wang <fwang@mandriva.org> 5.6-1.20080823.1mdv2009.0
+ Revision: 276118
- New patch series

* Sun Jul 13 2008 Funda Wang <fwang@mandriva.org> 5.6-1.20080705.1mdv2009.0
+ Revision: 234231
- revert  to previous path, as newer patch breaks building
- New patch series

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed May 21 2008 Funda Wang <fwang@mandriva.org> 5.6-1.20080517.1mdv2009.0
+ Revision: 209612
- New patches series

* Tue May 20 2008 Oden Eriksson <oeriksson@mandriva.com> 5.6-1.20071222.2mdv2009.0
+ Revision: 209479
- rebuilt with gcc43

  + Anssi Hannula <anssi@mandriva.org>
    - add ncursesw-devel provide

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sun Dec 23 2007 Funda Wang <fwang@mandriva.org> 5.6-1.20071222.1mdv2008.1
+ Revision: 137328
- New snapshot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Nov 07 2007 Funda Wang <fwang@mandriva.org> 5.6-1.20071103.1mdv2008.1
+ Revision: 106702
- patch updated to 20071103

* Tue Oct 30 2007 Funda Wang <fwang@mandriva.org> 5.6-1.20071020.1mdv2008.1
+ Revision: 103958
- add patch on 20071020

* Sun Oct 14 2007 Funda Wang <fwang@mandriva.org> 5.6-1.20071013.1mdv2008.1
+ Revision: 98261
- Patches updated on 20071013

* Tue Sep 18 2007 Anssi Hannula <anssi@mandriva.org> 5.6-1.20070901.3mdv2008.0
+ Revision: 89693
- rebuild due to package loss

* Fri Sep 07 2007 Funda Wang <fwang@mandriva.org> 5.6-1.20070901.2mdv2008.0
+ Revision: 81691
- fix conflict with kon2 package

* Tue Sep 04 2007 Funda Wang <fwang@mandriva.org> 5.6-1.20070901.1mdv2008.0
+ Revision: 79021
- Patch updated to 20070901

* Wed Aug 22 2007 Funda Wang <fwang@mandriva.org> 5.6-1.20070818.1mdv2008.0
+ Revision: 68756
- Patches updated to 20070818

* Fri Aug 10 2007 Funda Wang <fwang@mandriva.org> 5.6-1.20070728.1mdv2008.0
+ Revision: 61449
- add official 20070728 patch

* Tue Jul 24 2007 Funda Wang <fwang@mandriva.org> 5.6-1.20070721.1mdv2008.0
+ Revision: 55021
- Move cygwin and putty into main package
- do not provide old major
- Add patch on 20070721

* Wed Jul 18 2007 Funda Wang <fwang@mandriva.org> 5.6-1.20070716.2mdv2008.0
+ Revision: 53161
- Fix upgrading

* Tue Jul 17 2007 Funda Wang <fwang@mandriva.org> 5.6-1.20070716.1mdv2008.0
+ Revision: 52964
- New version
- New devel package policy
