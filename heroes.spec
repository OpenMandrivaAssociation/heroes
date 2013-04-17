%define	dataversion	1.5

Summary:	Game like Nibbles but different
Name:		heroes
Version:	0.21
Release:	11
Source0:	http://download.sourceforge.net/heroes/%{name}-%{version}.tar.bz2
Source1:	http://download.sourceforge.net/heroes/%{name}-data-%{dataversion}.tar.bz2
Source2:	http://download.sourceforge.net/heroes/%{name}-sound-tracks-1.0.tar.bz2
Source3:	http://download.sourceforge.net/heroes/%{name}-sound-effects-1.0.tar.bz2
Source5:	%{name}-16.png
Source6:	%{name}-32.png
Source7:	%{name}-48.png
Patch0:		%{name}-0.21-debian-fixes.patch.bz2
Patch1:		heroes-0.21-fix-build-gcc4.patch.bz2
License:	GPL
Url:		http://heroes.sourceforge.net/
Group:		Games/Arcade
BuildRequires:	gettext bison SDL-devel SDL_mixer-devel

%description
Heroes is similar to the "Tron" and "Nibbles" games of yore, but includes
many graphical improvements and new game features.  In it, you must
maneuver a small vehicle around a world and collect powerups while avoiding
obstacles, your opponents' trails, and even your own trail. Several modes
of play are available, including "get-all-the-bonuses", deathmatch, and
"squish-the-pedestrians".

%prep
%setup -q
%setup -q -D -T -a 1
%setup -q -D -T -a 2
%setup -q -D -T -a 3
%patch0 -p1
%patch1 -p1

cat <<EOF > %{name}.menu
?package(%{name}):command="%{_gamesbindir}/%{name}" \
		  icon=%{name}.png \
		  needs="x11" \
		  section="More Applications/Games/Arcade" \
		  title="Heroes"\
		  longtitle="%{Summary}" xdg="true"
EOF

cat << EOF > mandriva-%{name}.desktop
[Desktop Entry]
Encoding=UTF-8
Name=Heroes
Comment=%{summary}
Exec=%_gamesbindir/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

%build
%configure	--bindir=%{_gamesbindir} \
		--datadir=%{_gamesdatadir} \
		--disable-debug \
		--with-sdl
%make LDFLAGS="-lm -lpthread"
    (cd %{name}-data-%{dataversion}
     %configure	--bindir=%{_gamesbindir} --datadir=%{_gamesdatadir}
     %make
    )       
for i in sound-effects sound-tracks; do
    (
    cd %{name}-$i-1.0
    %configure --bindir=%{_gamesbindir} --datadir=%{_gamesdatadir}
		    
    %make
    )
done

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall bindir=$RPM_BUILD_ROOT%{_gamesbindir} datadir=$RPM_BUILD_ROOT%{_gamesdatadir}
    (cd %{name}-data-%{dataversion}
     %makeinstall bindir=$RPM_BUILD_ROOT%{_gamesbindir} datadir=$RPM_BUILD_ROOT%{_gamesdatadir}
    )
for i in sound-effects sound-tracks; do
    (
    cd %{name}-$i-1.0
    %makeinstall bindir=$RPM_BUILD_ROOT%{_gamesbindir} datadir=$RPM_BUILD_ROOT%{_gamesdatadir}
    )
done

mv $RPM_BUILD_ROOT%{_gamesdatadir}/locale/ $RPM_BUILD_ROOT%{_datadir}/
%find_lang %{name}

install -D -m644 mandriva-%{name}.desktop $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop
install -m644 %SOURCE6 -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %SOURCE5 -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %SOURCE7 -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%clean

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog INSTALL NEWS README THANKS TODO
%{_gamesdatadir}/%{name}
%{_mandir}/man6/%{name}*
%{_gamesbindir}/%{name}*
%{_datadir}/applications/*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_infodir}/%{name}.info*



%changelog
* Fri Sep 04 2009 Thierry Vignaud <tvignaud@mandriva.com> 0.21-8mdv2010.0
+ Revision: 429391
- rebuild

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 0.21-7mdv2009.0
+ Revision: 218432
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Thierry Vignaud <tvignaud@mandriva.com>
    - drop old menu
    - kill re-definition of %%buildroot on Pixel's request
    - import heroes

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Fri Jul  7 2006 Pixel <pixel@mandriva.com> 0.21-7mdv2007.0
- use mkrel
- switch to XDG menu

* Tue Oct 11 2005 Pixel <pixel@mandriva.com> 0.21-6mdk
- rebuild
- apply patch from debian (debian bug #297314)

* Thu Nov 20 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.21-5mdk
- merge in debian fixes (P0)
- fix buildrequires (lib64..)
- drop Packager tag
- minor cosmetics
- link against sdl

* Mon Aug 04 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.21-4mdk
- rebuild
- don't use overuse wildcards in %%files list
- change summary macro to avoid possible conflicts
- --disable-debug

* Sat Nov 23 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.21-3mdk
- add info page
- fix locales location

* Thu Nov 12 2002 Per Øyvind Karlsen <peroyvind@delonic.no> 0.21-2mdk
- Install stuff in the right places
- Remove obsolete Prefix tag
- Add menu item
- Add icons
- Cleanups

* Thu Jun 27 2002 Pixel <pixel@mandrakesoft.com> 0.21-1mdk
- new main release
- new data release

* Sat Feb  2 2002 Pixel <pixel@mandrakesoft.com> 0.19-1mdk
- new main version
- new data version

* Fri Oct 26 2001 Pixel <pixel@mandrakesoft.com> 0.15-1mdk
- new version

* Fri Oct 19 2001 Pixel <pixel@mandrakesoft.com> 0.14-1mdk
- new main version
- new data version

* Thu Oct 11 2001 Pixel <pixel@mandrakesoft.com> 0.12-3mdk
- s/Copyright/License/
- fix rights on sources

* Thu Jul 12 2001 Daouda LO <daouda@mandrakesoft.com> 0.12-2mdk
- update heroes source data to 1.1.
- provides mising icons.

* Wed Jul 11 2001  Daouda Lo <daouda@mandrakesoft.com> 0.12-1mdk
- new version.

* Tue Jul  3 2001 Pixel <pixel@mandrakesoft.com> 0.11-1mdk
- new version

* Mon May 14 2001 Pixel <pixel@mandrakesoft.com> 0.10-2mdk
- rebuild with new SDL

* Tue May  8 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 0.10-1mdk
- version 0.10

* Mon Mar  5 2001 Pixel <pixel@mandrakesoft.com> 0.9-2mdk
- add mo files (thanks to Alexandre Duret-Lutz)

* Sat Mar  3 2001 Pixel <pixel@mandrakesoft.com> 0.9-1mdk
- new version

* Wed Dec 20 2000 Pixel <pixel@mandrakesoft.com> 0.8-1mdk
- new version

* Tue Dec 19 2000 Pixel <pixel@mandrakesoft.com> 0.7-2mdk
- rebuild with new libSDL_mixer

* Wed Nov 29 2000 Pixel <pixel@mandrakesoft.com> 0.7-1mdk
- initial spec
