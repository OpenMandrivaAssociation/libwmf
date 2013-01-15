%define api 0.2
%define major	7
%define libname %mklibname wmf%{api}_ %major
%define litename %mklibname wmflite%{api}_ %major
%define develname %mklibname -d wmf

Summary:	A library to convert wmf files
Name:		libwmf
Version:	0.2.8.4
Release:	26
License:	GPL
Group:		Text tools
URL:		http://sourceforge.net/projects/wvware/
Source0:	http://download.sourceforge.net/wvware/%{name}-%{version}.tar.bz2
Patch0:		libwmf-0.2.7-libwmf-config.patch
Patch1:		libwmf-0.2.8.3-CAN-2004-0941.patch
Patch2:		libwmf-0.2.8.3-CAN-2004-0990.patch
Patch3:		libwmf-0.2.8.4-intoverflow.patch
Patch4:		libwmf-0.2.8.4-CVE2007-2756.patch
Patch5:		libwmf-0.2.8.4-rh-CVE-2009-1364.diff
Patch6:		libwmf-0.2.8.4-gdk2.22.patch
Patch7:		libwmf-automake-1.13.patch

BuildRequires:	expat-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(x11)
Requires(post):	gdk-pixbuf2.0
Requires(postun): gdk-pixbuf2.0
Requires:	urw-fonts

%description
libwmf is a library for unix like machines that can convert wmf
files into other formats, currently it supports a gd binding
to convert to gif, and an X one to draw direct to an X window
or pixmap.

%package -n %{libname}
Summary:	A library to convert wmf files. - library files
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with libwmf.

%package -n %{litename}
Summary:	A library to convert wmf files. - library files
Group:		System/Libraries

%description -n %{litename}
This package contains the library needed to run programs dynamically
linked with libwmflite.

%package -n %{develname}
Summary:	A library to convert wmf files. - development environment
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	libwmf-devel = %{version}-%{release}
Obsoletes:	libwmf-devel < %{version}-%{release}
Obsoletes:	%{_lib}wmf0.2_7-devel < 0.2.8.4-21

%description -n %{develname}
libwmf is a library for unix like machines that can convert wmf
files into other formats, currently it supports a gd binding
to convert to gif, and an X one to draw direct to an X window
or pixmap.

Install libwmf-devel if you need to compile an application with libwmf
support.

%prep
%setup -q
%patch0 -p1 -b .fpons
%patch1 -p1 -b .can-2004-0941
%patch2 -p1 -b .can-2004-0990
%patch3 -p1 -b .cve-2006-3376
%patch4 -p1 -b .cve-2007-2756
%patch5 -p0 -b .CVE-2009-1364
%patch6 -p0 -b .gdk222
%patch7 -p1 -b .am113~

%build
autoreconf -fi
%configure2_5x \
	--disable-static

%make

%install
rm -rf %{buildroot} installed-docs
%makeinstall_std

mv %{buildroot}%{_prefix}/share/doc/* installed-docs

#gw no windows line endings
perl -pi -e 's/\r//' $(find installed-docs -type f )

# remove anything relevant to fonts.
rm -rf %{buildroot}%{_bindir}/libwmf-fontmap %{buildroot}%{_datadir}/libwmf

# multiarch support
%multiarch_binaries %{buildroot}%{_bindir}/libwmf-config

%files
%docdir COPYING
%{_bindir}/wmf2*
%{_libdir}/gdk-pixbuf-2.0/*/loaders/io-wmf.*

%files -n %{libname}
%{_libdir}/libwmf-%{api}.so.%{major}*

%files -n %{litename}
%{_libdir}/libwmflite-%{api}.so.%{major}*

%files -n %{develname}
%doc CREDITS README NEWS ChangeLog
%doc installed-docs/*
%{_bindir}/libwmf-config
%{multiarch_bindir}/libwmf-config
%{_libdir}/libwmf.so
%{_libdir}/libwmflite.so
%{_includedir}/libwmf



%changelog
* Fri May 11 2012 Alexander Khrukin <akhrukin@mandriva.org> 0.2.8.4-26
+ Revision: 798257
- rel bump and rebuild

* Tue Nov 22 2011 Matthew Dawkins <mattydaw@mandriva.org> 0.2.8.4-25
+ Revision: 732478
- fixed p0 naming
- rebuild
- moved gdk_pixbuf loader libs to main pkg
- removed .la files
- split out lite lib
- removed dup doc files across sub pkgs
- remove defattr
- removed dup post/un scriptlets, handled by gdk-pixbuf triggers
- removed old ldconfig scriptlets
- removed clean section
- cleaned up spec
- removed old conflicts/provides
- converted BRs to pkgconfig provides
- removed mkrel & BuildRoot

* Thu Sep 29 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 0.2.8.4-24
+ Revision: 701829
- rebuild for new libpng15

* Fri Apr 29 2011 Funda Wang <fwang@mandriva.org> 0.2.8.4-23
+ Revision: 660667
- fix usage of multiarch

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Thu Jul 29 2010 Funda Wang <fwang@mandriva.org> 0.2.8.4-22mdv2011.0
+ Revision: 563204
- add patch to build with gdk 2.22

* Thu Jul 29 2010 Funda Wang <fwang@mandriva.org> 0.2.8.4-21mdv2011.0
+ Revision: 563183
- new devel package name policy
- adopt to gdk and gtk splitting

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.8.4-20mdv2010.1
+ Revision: 488786
- rebuilt against libjpeg v8

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2.8.4-19mdv2010.0
+ Revision: 416524
- rebuilt against libjpeg v7

* Tue May 05 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2.8.4-18mdv2010.0
+ Revision: 372264
- P5: security fix for CVE-2009-1364 (redhat)

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0.2.8.4-17mdv2009.0
+ Revision: 223041
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2.8.4-16mdv2008.1
+ Revision: 179016
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Jun 15 2007 Jérôme Soyer <saispo@mandriva.org> 0.2.8.4-14mdv2008.0
+ Revision: 40000
- Bump release
- Fix bug #31483

* Fri Jun 08 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 0.2.8.4-13mdv2008.0
+ Revision: 37261
- rebuild for expat
- spec file clean

