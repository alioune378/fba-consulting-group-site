(function(){
var d=document,$=function(s,r){return (r||d).querySelector(s)},$$=function(s,r){return [].slice.call((r||d).querySelectorAll(s))};
d.documentElement.classList.add('js');
var y=$('#yr');if(y)y.textContent=new Date().getFullYear();
/* mobile nav */
var b=$('.burger'),n=$('#nav');
function setNav(o){n.classList.toggle('is-open',o);d.body.classList.toggle('nav-open',o);b.setAttribute('aria-expanded',o);b.setAttribute('aria-label',o?'Fermer le menu':'Ouvrir le menu')}
if(b&&n){b.addEventListener('click',function(){setNav(!n.classList.contains('is-open'))});
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&n.classList.contains('is-open')){setNav(false);b.focus()}});
$$('a',n).forEach(function(a){a.addEventListener('click',function(){setNav(false)})});
matchMedia('(min-width:1061px)').addEventListener('change',function(m){if(m.matches)setNav(false)})}
/* header shadow once scrolled */
var hd=$('.header'),hs=function(){hd&&hd.classList.toggle('is-scrolled',scrollY>8)};hs();addEventListener('scroll',hs,{passive:true});
/* reveal */
var rv=$$('.reveal'),reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
/* stagger siblings revealed together */
rv.forEach(function(el){var sib=[].filter.call(el.parentNode.children,function(c){return c.classList.contains('reveal')});var i=sib.indexOf(el);if(i>0)el.style.setProperty('--d',Math.min(i,5)*0.08+'s')});
if('IntersectionObserver' in window&&!reduce){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});rv.forEach(function(el){io.observe(el)})}else rv.forEach(function(el){el.classList.add('in')});
setTimeout(function(){rv.forEach(function(el){el.classList.add('in')})},4000);
/* counters */
var fmt=new Intl.NumberFormat('fr-FR');
$$('[data-count]').forEach(function(el){var t=+el.dataset.count,p=el.dataset.prefix||'',s=el.dataset.suffix||'';
 var final=p+fmt.format(t)+s;el.textContent=final;if(reduce||!('IntersectionObserver' in window))return;
 var o=new IntersectionObserver(function(es){if(!es[0].isIntersecting)return;o.disconnect();var st=performance.now(),du=1400;
  (function f(now){var k=Math.min(1,(now-st)/du),v=Math.round(t*(1-Math.pow(1-k,3)));el.textContent=p+fmt.format(v)+s;if(k<1)requestAnimationFrame(f);else el.textContent=final})(st)},{threshold:.5});o.observe(el)});
/* whatsapp button: step aside over forms, CTA bands and footer, and while typing */
var wf=$('.wa-float');if(wf&&'IntersectionObserver' in window){var seen=new Set(),down=false,ly=scrollY,upd=function(){var typing=d.activeElement&&/^(INPUT|TEXTAREA|SELECT)$/.test(d.activeElement.tagName);wf.classList.toggle('is-hidden',seen.size>0||!!typing||down)};
 addEventListener('scroll',function(){var y=scrollY,dy=y-ly;if(Math.abs(dy)>8){down=dy>0&&y>300;ly=y;upd()}},{passive:true});
 var wo=new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?seen.add(e.target):seen.delete(e.target)});upd()});$$('.form,.cta,.footer,.t-cta,.paths,.hero-cta,.proof-dlg').forEach(function(el){wo.observe(el)});d.addEventListener('focusin',upd);d.addEventListener('focusout',function(){setTimeout(upd,50)})}
/* proof lightbox (falls back to opening the image) */
$$('[data-dialog]').forEach(function(a){var dl=d.getElementById(a.dataset.dialog);if(!dl||!dl.showModal)return;a.addEventListener('click',function(ev){ev.preventDefault();dl.showModal()})});
$$('dialog').forEach(function(dl){dl.addEventListener('click',function(ev){if(ev.target===dl||ev.target.closest('[data-close]'))dl.close()})});
/* testimonial filters */
$$('.tfilters').forEach(function(g){var bs=$$('.tf',g),cards=$$('.tcard',g.parentNode);bs.forEach(function(bt){bt.addEventListener('click',function(){var v=bt.dataset.filter;bs.forEach(function(x){var on=x===bt;x.classList.toggle('is-on',on);x.setAttribute('aria-pressed',on)});cards.forEach(function(c){c.classList.toggle('is-hidden',v!=='all'&&c.dataset.cat!==v)})})})});
/* testimonials: read more on mobile */
var tq=matchMedia('(max-width:759px)');function clampT(){$$('.tcard').forEach(function(c){var p=$('blockquote p',c),bt=$('.t-more',c);if(!p||!bt)return;if(bt.getAttribute('aria-expanded')==='true')return;c.classList.add('is-clamped');var over=tq.matches&&p.scrollHeight>p.clientHeight+2;bt.hidden=!over;if(!over)c.classList.remove('is-clamped')})}
$$('.t-more').forEach(function(bt){bt.addEventListener('click',function(){var c=bt.closest('.tcard'),o=bt.getAttribute('aria-expanded')!=='true';c.classList.toggle('is-clamped',!o);bt.setAttribute('aria-expanded',o);bt.textContent=o?'Réduire':'Lire la suite'})});
clampT();tq.addEventListener('change',clampT);addEventListener('load',clampT);
/* parcours: show all */
$$('.pc-toggle').forEach(function(bt){var w=bt.closest('.pc-wrap');bt.hidden=false;bt.addEventListener('click',function(){var o=w.classList.toggle('is-open');bt.setAttribute('aria-expanded',o);bt.textContent=o?'Réduire le parcours':'Voir tout le parcours';if(!o)w.scrollIntoView({block:'start'})})});
/* forms */
var qs=new URLSearchParams(location.search),svc=qs.get('service');if(svc){var sel=$('#d-svc');if(sel)for(var i=0;i<sel.options.length;i++)if(sel.options[i].text===svc)sel.selectedIndex=i}
$$('form.form').forEach(function(f){
 var t=$('input[name=t]',f);if(t)t.value=Date.now();
 var st=$('.status',f);
 function clr(){$$('.f',f).forEach(function(x){x.classList.remove('has-err');var m=$('.err',x);if(m)m.remove()})}
 function bad(el,msg){var w=el.closest('.f');w.classList.add('has-err');var m=d.createElement('span');m.className='err';m.id=el.id+'-e';m.textContent=msg;w.appendChild(m);el.setAttribute('aria-describedby',m.id);el.setAttribute('aria-invalid','true')}
 f.addEventListener('submit',function(ev){ev.preventDefault();clr();st.className='status';st.textContent='';var first=null,ok=true;
  $$('input,select,textarea',f).forEach(function(el){el.removeAttribute('aria-invalid');if(el.type==='hidden'||el.name==='bot-field')return;var v=(el.type==='checkbox')?el.checked:(el.type==='file'?(el.files&&el.files.length?'f':''):el.value.trim()),msg='';
   if(el.required&&!v)msg=el.type==='checkbox'?'Veuillez accepter pour continuer.':'Ce champ est obligatoire.';
   else if(el.type==='email'&&v&&!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v))msg='Adresse e-mail invalide.';
   else if(el.type==='tel'&&v&&v.replace(/\D/g,'').length<8)msg='Numéro invalide (8 chiffres minimum).';
   else if(el.minLength>0&&v&&v.length<el.minLength)msg='Merci de détailler un peu plus ('+el.minLength+' caractères minimum).';
   else if(el.type==='file'&&el.files&&el.files[0]){var fl=el.files[0],okx=/\.(pdf|docx?)$/i.test(fl.name);if(!okx)msg='Format accepté : PDF, DOC ou DOCX.';else if(fl.size>(+el.dataset.max||7340032))msg='Fichier trop volumineux (7 Mo maximum).'}
   if(msg){ok=false;bad(el,msg);if(!first)first=el}});
  if(!ok){st.className='status bad';st.textContent='Veuillez corriger les champs signalés.';first.focus();return}
  if($('[name=bot-field]',f).value||Date.now()-(+t.value)<2500){st.className='status ok';st.textContent='Merci.';return}
  var btn=$('button[type=submit]',f);btn.disabled=true;var label=btn.textContent;btn.textContent='Envoi en cours…';
  var fd=new FormData(f),hasFile=false;$$('input[type=file]',f).forEach(function(x){if(x.files&&x.files.length)hasFile=true});var body=hasFile?fd:new URLSearchParams(fd).toString();
  var done=function(good){btn.disabled=false;btn.textContent=label;
   if(good){f.reset();st.className='status ok';st.textContent=f.name==='rendez-vous'?'Demande reçue. Votre rendez-vous n’est pas encore confirmé : FBA Consulting Group vous répondra pour confirmer ou proposer un autre créneau.':(f.name==='candidature'?'Merci, votre candidature a bien été reçue. Aucune information ne sera publiée sans votre accord écrit explicite.':'Merci, votre demande a bien été reçue. Nous vous répondrons prochainement.')}
   else{st.className='status bad';st.textContent='Votre demande n’a pas pu être envoyée. Veuillez réessayer ou nous écrire sur WhatsApp.'}};
  if(f.dataset.mode!=='netlify'){btn.disabled=false;btn.textContent=label;st.className='status bad';st.textContent='Mode démonstration : aucune demande n’a été envoyée.';return}
  fetch('/',hasFile?{method:'POST',body:body}:{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:body}).then(function(r){done(r.ok)}).catch(function(){done(false)})})});
})();
