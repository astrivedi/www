require 'yaml'
require 'json'
require 'cgi'
require 'fileutils'
require 'kramdown'

ROOT = File.expand_path(__dir__)
SRC = File.join(ROOT, 'source')
OUT = File.dirname(ROOT)
ORIGIN = 'https://ashutoshtrivedi.com'
LINKS = YAML.load_file(File.join(SRC, '_config.yml'))['links']
NAV = [['Home','/'],['Research','/research/'],['Publications','/publications/'],['People','/students/'],['Teaching','/teaching/'],['Talks','/talks/'],['CV','/cv/']]
$routes = []
def esc(s); CGI.escapeHTML(s.to_s); end
def md(s)
  Kramdown::Document.new(s.to_s.gsub(/:contentReference\[.*?\]\{.*?\}/, '')).to_html
end
def page(path, title, description, body, extra = '')
  url = ORIGIN + path
  full_title = path == '/' ? 'Ashutosh Trivedi | Computer Science · CU Boulder' : "#{title} | Ashutosh Trivedi"
  person = {'@context'=>'https://schema.org','@type'=>'ProfilePage','@id'=>url+'#page','url'=>url,'name'=>full_title,'mainEntity'=>{'@type'=>'Person','@id'=>ORIGIN+'/#person','name'=>'Ashutosh Trivedi','url'=>ORIGIN+'/','image'=>ORIGIN+'/assets/img/ashutosh.jpeg','jobTitle'=>'Associate Professor of Computer Science','affiliation'=>{'@type'=>'CollegeOrUniversity','name'=>'University of Colorado Boulder','url'=>'https://www.colorado.edu/'},'email'=>'mailto:ashutosh.trivedi@colorado.edu','sameAs'=>[LINKS['scholar'],LINKS['dblp']],'knowsAbout'=>['Formal Methods','Reinforcement Learning','Trustworthy AI','Medical and Cyber-Physical Systems']}}
  nav = NAV.map{|name,href| "<a href=\"#{href}\"#{path == href ? ' aria-current="page"' : ''}>#{esc(name)}</a>"}.join("\n")
  html = <<~HTML
  <!doctype html>
  <html lang="en">
  <head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>#{esc(full_title)}</title>
  <meta name="description" content="#{esc(description)}">
  <link rel="canonical" href="#{url}">
  <meta property="og:type" content="#{path.start_with?('/papers/') ? 'article' : 'website'}">
  <meta property="og:title" content="#{esc(full_title)}">
  <meta property="og:description" content="#{esc(description)}">
  <meta property="og:url" content="#{url}">
  <meta property="og:site_name" content="Ashutosh Trivedi">
  <link rel="stylesheet" href="/assets/site.css">
  <script type="application/ld+json">#{JSON.generate(person).gsub('<','\\u003c')}</script>
  #{extra}
  </head>
  <body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header><nav aria-label="Main navigation">#{nav}</nav></header>
  <main id="main">#{body}</main>
  <footer><p>Ashutosh Trivedi · University of Colorado Boulder<br><a href="mailto:ashutosh.trivedi@colorado.edu">ashutosh.trivedi@colorado.edu</a></p></footer>
  </body>
  </html>
  HTML
  file = path.end_with?('/') ? File.join(OUT,path,'index.html') : File.join(OUT,path)
  FileUtils.mkdir_p(File.dirname(file))
  File.write(file,html)
  $routes << path
end

FileUtils.mkdir_p(File.join(OUT,'assets/img'))
FileUtils.cp(File.join(ROOT, 'site.css'), File.join(OUT, 'assets/site.css'))
FileUtils.cp(File.join(SRC,'assets/img/ashutosh.jpeg'), File.join(OUT,'assets/img/ashutosh.jpeg'))
FileUtils.cp(File.join(SRC,'assets/AshutoshTrivedi_CV.pdf'), File.join(OUT,'assets/AshutoshTrivedi_CV.pdf'))
FileUtils.cp_r(File.join(SRC,'assets/papers'),File.join(OUT,'assets'))

PAPERS = Dir[File.join(SRC,'_papers/*.md')].map do |f|
  p = YAML.load(File.read(f).split(/^---\s*$\n?/)[1]); p['slug'] = File.basename(f,'.md'); p
end.sort_by{|p| [-p['year'],p['title']]}
# Repair the empty supplied citation using only the supplied bibliographic fields.
PAPERS.each do |p|
  bib=File.join(OUT,'assets/papers',p['slug']+'.bib')
  if !File.exist?(bib) || File.zero?(bib)
    File.write(bib,"@inproceedings{#{p['slug']},\n  title = {#{p['title']}},\n  author = {#{p['authors'].join(' and ')}},\n  booktitle = {#{p['venue'].gsub(/[{}]/,'')}},\n  year = {#{p['year']}}\n}\n")
  end
end
def resources(p)
  %w[pdf arxiv doi code bibtex slides video].map do |key|
    href = p[key].to_s.strip
    next if href.empty?
    href = '/'+href unless href.start_with?('/','https://','http://')
    href = href.sub('/22025-neus','/2025-neus')
    next if href.start_with?('/') && (!File.file?(OUT+href) || File.zero?(OUT+href))
    label = {'pdf'=>'Paper (PDF)','arxiv'=>(href.include?('arxiv.org') ? 'arXiv' : 'Proceedings'),'doi'=>'Publisher','code'=>'Code','bibtex'=>'BibTeX','slides'=>'Slides','video'=>'Video'}[key]
    "<a href=\"#{esc(href)}\">#{label}</a>"
  end.compact.join(' <span aria-hidden="true">·</span> ')
end
def venue(p)
  v=p['venue'].gsub(/[{}]/,'').strip
  return 'Findings of ACL, 2025' if p['slug'].include?('2025-acl')
  return 'ICSE, 2025' if p['slug'].include?('2025-icse')
  return 'IJCAI, 2025' if p['slug'].include?('2025-ijcai')
  v.include?(p['year'].to_s) ? v : "#{v}, #{p['year']}"
end
def entry(p)
  "<li class=\"publication\" id=\"#{p['slug']}\"><article><h3><a href=\"/papers/#{p['slug']}/\">#{esc(p['title'])}</a></h3><p>#{p['authors'].map{|a| a == 'Ashutosh Trivedi' ? '<strong>Ashutosh Trivedi</strong>' : esc(a)}.join(', ')}.</p><p><em>#{esc(venue(p))}</em>#{p['award'] ? '<br><span class="award">'+esc(p['award'])+'</span>' : ''}</p><p class=\"resources\">#{resources(p)}</p></article></li>"
end
NEWS = YAML.load_file(File.join(SRC,'_data/news.yml'))
def news_rows(items)
  '<ul class="news">'+items.map{|n| '<li><time datetime="'+(n['datetime'] || Date.strptime(n['date'],'%b %Y').strftime('%Y-%m'))+'">'+esc(n['date'])+'</time><div>'+n['text']+'</div></li>'}.join+'</ul>'
end
selected = ['2024-cav-regular-rl','2025-neus-stochastic-neural-simulation','2022-neurips-rrl']
home = <<~HTML
<section class="intro" aria-labelledby="name">
<div><h1 id="name">Ashutosh Trivedi</h1><p class="affiliation">Associate Professor of Computer Science<br>University of Colorado Boulder</p>
<p>I work on formal methods for reinforcement learning, trustworthy AI, and safety-critical software and cyber-physical systems.</p>
<p>My research combines verification, learning, and symbolic reasoning to make intelligent systems safer, fairer, and easier to explain.</p>
<p class="profile-links"><a href="/cv/">CV</a> · <a href="#{LINKS['scholar']}">Google Scholar</a> · <a href="#{LINKS['github']}" aria-label="GitHub — CUPLV research group">GitHub</a> · <a href="https://www.colorado.edu/cs/">CU Boulder</a></p></div>
<img src="/assets/img/ashutosh.jpeg" width="220" height="220" alt="Portrait of Ashutosh Trivedi" fetchpriority="high">
</section>
<section aria-labelledby="news"><h2 id="news">News</h2>#{news_rows(NEWS.select { |item| item['featured'] }.first(4))}<p class="more"><a href="/news/">All news</a></p></section>
<section aria-labelledby="research"><h2 id="research">Research</h2><ul class="research-index"><li><a href="/research/#formal-methods">Formal Methods</a></li><li><a href="/research/#reinforcement-learning">Reinforcement Learning</a></li><li><a href="/research/#trustworthy-ai">Trustworthy AI</a></li><li><a href="/research/#medical-and-cyber-physical-systems">Medical and Cyber-Physical Systems</a></li></ul></section>
<section aria-labelledby="selected"><h2 id="selected">Selected Publications</h2><ol class="publications">#{selected.map{|slug| entry(PAPERS.find{|p| p['slug']==slug})}.join}</ol><p class="more"><a href="/publications/">All publications</a></p></section>
<section aria-labelledby="students"><h2 id="students">Students</h2><p>I work with students and postdoctoral researchers in the <a href="https://plv.colorado.edu/">Programming Languages and Verification (CUPLV)</a> group.</p><p><a href="/students/">Current students, collaborators, and alumni</a></p></section>
<section aria-labelledby="teaching"><h2 id="teaching">Teaching</h2><p>I teach theoretical computer science, reinforcement learning, and cyber-physical systems.</p><p><a href="/teaching/">Courses and teaching history</a></p></section>
HTML
page('/','Home','Ashutosh Trivedi, Associate Professor of Computer Science at CU Boulder. Research in formal methods, reinforcement learning, trustworthy AI, and cyber-physical systems.',home)

def source_body(file)
  s=File.read(File.join(SRC,file)).split(/^---\s*$\n?/,3).last
  s.gsub!(/<h1>.*?<\/h1>/m,'')
  LINKS.each{|k,v| s.gsub!("{{ site.links.#{k} }}",v)}
  s.gsub!('/group/','/students/')
  md(s)
end

# Research-page references use the same records and venue formatter as publications.
def research_paper(slug)
  PAPERS.find { |paper| paper['slug'] == slug } or raise "Unknown paper: #{slug}"
end

def research_link(slug, label = nil)
  paper = research_paper(slug)
  "<a href=\"/papers/#{paper['slug']}/\">#{esc(label || paper['title'])}</a>"
end

def research_venue(slug)
  paper = research_paper(slug)
  ["<span class=\"research-venue\">#{esc(venue(paper))}</span>", paper['award'] && esc(paper['award'])].compact.join(' · ')
end

def representative_work(slugs)
  '<p class="representative-label"><strong>Representative work:</strong></p><ul class="representative-work" role="list">' +
    slugs.map { |slug| "<li>#{research_link(slug)} <span class=\"research-citation\">— #{research_venue(slug)}</span></li>" }.join + '</ul>'
end

research = <<~HTML
<div class="research-page">
<h1>Research</h1>
<p class="research-vision"><strong>How can we build learning-enabled systems whose behavior can be specified, verified, and trusted?</strong></p>
<p>My research brings together formal methods, reinforcement learning, and software analysis. I develop mathematical foundations, algorithms, and tools for reasoning about intelligent systems operating under uncertainty, particularly when their decisions have safety, legal, or societal consequences.</p>
<p>My work is organized around three connected goals: extending the foundations of sequential decision-making, providing formal guarantees for learning-enabled systems, and making consequential AI-driven software auditable and explainable.</p>
<p class="research-summary"><strong>Foundations · Guarantees · Accountability</strong></p>

<section class="research-program" aria-labelledby="formal-foundations">
<span id="formal-methods" aria-hidden="true"></span><span id="reinforcement-learning" aria-hidden="true"></span>
<h2 id="formal-foundations">Formal Foundations of Reinforcement Learning</h2>
<p>Classical reinforcement learning often assumes finite-state environments, simple reward objectives, and episodic interaction. I develop foundations and algorithms for settings in which agents must satisfy richer temporal requirements, operate in structured or recursive environments, or interact with continuous-time physical systems.</p>
<ul class="research-directions">
<li>Reinforcement learning with temporal and omega-regular objectives</li>
<li>Regular languages, automata, and reward machines</li>
<li>Recursive and branching decision processes</li>
<li>Continuous-time and physically grounded reinforcement learning</li>
<li>History-dependent and nonstandard discounting models</li>
</ul>
#{representative_work(%w[2024-cav-regular-rl 2022-neurips-rrl 2019-tacas-omega-rl 2025-ijcai-continuous-time-rewards])}
</section>

<section class="research-program" aria-labelledby="verified-learning-control">
<span id="medical-and-cyber-physical-systems" aria-hidden="true"></span>
<h2 id="verified-learning-control">Verified Learning and Control</h2>
<p>Learning-enabled controllers must operate safely even when their environments are uncertain and their learned models are imperfect. I develop certificates, abstractions, and runtime mechanisms that connect formal verification with learning and control.</p>
<ul class="research-directions">
<li>Barrier, Lyapunov, and closure certificates</li>
<li>Formal abstractions and simulation relations</li>
<li>Safe transfer between learned controllers</li>
<li>Runtime monitoring and shielding for reinforcement learning</li>
<li>Safety-critical applications, including medical devices and cardiac control</li>
</ul>
<p>Safe reinforcement learning for cardiac pacing, including the use of cardiac digital twins to evaluate pacing strategies, is an active research direction.</p>
#{representative_work(%w[2025-neus-stochastic-neural-simulation 2024-hscc-closure-certificates])}
</section>

<section class="research-program" aria-labelledby="auditable-ai-software">
<span id="trustworthy-ai" aria-hidden="true"></span>
<h2 id="auditable-ai-software">Auditable AI and Software</h2>
<p>When software affects legal, financial, medical, or social outcomes, failures must be detectable and decisions must be open to scrutiny. I develop formal and data-driven methods for testing, explaining, and improving AI-driven software when complete specifications are unavailable.</p>
<p>This program also studies how learning and large language models can be combined with logic, automata, program analysis, and symbolic solvers to produce reasoning that is structured and auditable rather than merely plausible.</p>
<ul class="research-directions">
<li>Fairness testing and discrimination discovery</li>
<li>Metamorphic and relational testing</li>
<li>Neurosymbolic reasoning and proof-guided explanation</li>
<li>Regulatory and legal accountability</li>
<li>Explanation of sequential and combinatorial reasoning</li>
</ul>
#{representative_work(%w[2025-icse-fairness-evt 2025-ase-discrimination-clusters 2023-icse-seis-tax-prep 2025-arxiv-hitori 2025-acl-explaining-puzzles])}
</section>

<section class="research-contributions" aria-labelledby="selected-contributions">
<h2 id="selected-contributions">Selected Contributions</h2>
<ol class="contribution-list" role="list">
<li><h3>#{research_link('2024-cav-regular-rl')}</h3>
<p>A symbolic framework for reinforcement learning that represents sets of states with regular languages and transitions with rational transductions.</p>
<p class="research-citation">#{research_venue('2024-cav-regular-rl')}</p></li>
<li><h3>#{research_link('2022-neurips-rrl')}</h3>
<p>Foundations for learning in recursive decision processes whose executions can have an unbounded call structure.</p>
<p class="research-citation">#{research_venue('2022-neurips-rrl')}</p></li>
<li><h3>#{research_link('2024-hscc-closure-certificates', 'Certificates for Learning-Enabled Control')}</h3>
<p>Certificate-based methods for reasoning about continuous and stochastic dynamical systems.</p>
<p class="research-citation">#{research_link('2024-hscc-closure-certificates')} (#{esc(venue(research_paper('2024-hscc-closure-certificates')))}) · #{research_link('2025-neus-stochastic-neural-simulation')} (#{esc(venue(research_paper('2025-neus-stochastic-neural-simulation')))})</p></li>
<li><h3>#{research_link('2023-icse-seis-tax-prep', 'Testing Consequential Software')}</h3>
<p>Methods for detecting systematic failures and discrimination when a complete behavioral specification is unavailable.</p>
<p class="research-citation">#{research_link('2023-icse-seis-tax-prep', 'Tax preparation software')} (#{esc(venue(research_paper('2023-icse-seis-tax-prep')))}) · #{research_link('2025-icse-fairness-evt')} (#{esc(venue(research_paper('2025-icse-fairness-evt')))})</p></li>
</ol>
</section>
<p class="research-all"><a href="/publications/">View all publications <span aria-hidden="true">→</span></a></p>
</div>
HTML
page('/research/','Research','Ashutosh Trivedi’s research on formal methods for reinforcement learning, verified learning and control, trustworthy AI, and auditable software.',research)
years=PAPERS.map{|p|p['year']}.uniq
pubs='<h1>Publications</h1><p>Papers with full bibliographic entries and available manuscripts. See also <a href="'+LINKS['scholar']+'">Google Scholar</a>, <a href="'+LINKS['dblp']+'">DBLP</a>, and my <a href="/cv/">CV</a>.</p>'
pubs+='<nav class="year-nav" aria-label="Publication years">'+years.map{|y|"<a href=\"#year-#{y}\">#{y}</a>"}.join+'</nav>'
years.each{|y|pubs+="<section aria-labelledby=\"year-#{y}\"><h2 id=\"year-#{y}\">#{y}</h2><ol class=\"publications\">"+PAPERS.select{|p|p['year']==y}.map{|p|entry(p)}.join+'</ol></section>'}
page('/publications/','Publications','Publications by Ashutosh Trivedi and collaborators, with authors, venues, paper PDFs, arXiv, and BibTeX citations.',pubs)
PAPERS.each do |p|
  extra='<meta name="citation_title" content="'+esc(p['title'])+'">'+p['authors'].map{|a|'<meta name="citation_author" content="'+esc(a)+'">'}.join+'<meta name="citation_publication_date" content="'+p['year'].to_s+'"><meta name="citation_pdf_url" content="'+ORIGIN+'/'+p['pdf'].strip.sub(/^\//,'')+'"><meta name="citation_conference_title" content="'+esc(venue(p))+'">'
  extra+='<script type="application/ld+json">'+JSON.generate({'@context'=>'https://schema.org','@type'=>'ScholarlyArticle','headline'=>p['title'],'author'=>p['authors'].map{|a|{'@type'=>'Person','name'=>a}},'datePublished'=>p['year'].to_s,'url'=>ORIGIN+'/papers/'+p['slug']+'/'}).gsub('<','\\u003c')+'</script>'
  body='<p class="back"><a href="/publications/">Publications</a></p><h1>'+esc(p['title'])+'</h1><p>'+esc(p['authors'].join(', '))+'.</p><p><em>'+esc(venue(p))+'</em></p>'
  body+='<p>'+esc(p['award'])+'</p>' if p['award']
  body+='<p class="resources">'+resources(p)+'</p><h2>Abstract</h2>'+md(p['abstract'])
  page('/papers/'+p['slug']+'/',p['title'],p['title']+'. '+p['authors'].join(', ')+'. '+venue(p)+'.',body,extra)
end
students=source_body('group.md')
page('/students/','People','Students, postdoctoral researchers, and alumni working with Ashutosh Trivedi in the CUPLV group at CU Boulder.','<h1>People</h1>'+students)
teaching=source_body('teaching.md')
page('/teaching/','Teaching','Courses taught by Ashutosh Trivedi at CU Boulder and IIT Bombay, including theory of computation, reinforcement learning, and cyber-physical systems.','<h1>Teaching</h1>'+teaching)
page('/talks/','Talks','Talks and available presentation materials from Ashutosh Trivedi’s research.','<h1>Talks</h1><h2>Seminars</h2><article><h3>Hyperproperties</h3><p>DIMAP seminar, University of Warwick<br><time datetime="2025-06">June 2025</time></p></article><h2>Presentation materials</h2><article><h3>Uncovering Discrimination Clusters: Quantifying and Explaining Systematic Fairness Violations</h3><p>ASE 2025</p><p><a href="/assets/papers/2025-ase-discrimination-clusters.pptx">Slides (PowerPoint)</a> · <a href="/papers/2025-ase-discrimination-clusters/">Paper and authors</a></p></article>')
page('/cv/','Curriculum Vitae','Curriculum vitae and academic background of Ashutosh Trivedi, Associate Professor of Computer Science at CU Boulder.','<h1>Curriculum Vitae</h1><p><a href="/assets/AshutoshTrivedi_CV.pdf">Download CV (PDF)</a></p><h2>Academic background</h2><p>I received my Ph.D. in Computer Science from the University of Warwick, specializing in game theory and quantitative verification. Before joining CU Boulder, I held academic positions at IIT Bombay, the University of Pennsylvania, and the University of Oxford.</p><h2>Recognition</h2><ul><li>NSF CAREER Award, 2022</li><li>Royal Society Wolfson Visiting Fellowship, 2024</li><li>Distinguished Paper Award, CAV 2024, for <a href="/papers/2024-cav-regular-rl/">Regular Reinforcement Learning</a></li></ul><p>See my <a href="/publications/">publications</a>, <a href="/teaching/">teaching</a>, and <a href="/students/">students and alumni</a> for further details.</p>')
page('/news/','News','Dated research, teaching, student, and award announcements from Ashutosh Trivedi.','<h1>News</h1>'+news_rows(NEWS))
page('/bio/','Biography','Academic biography of Ashutosh Trivedi.','<h1>Biography</h1>'+source_body('bio.md'))
page('/contact/','Contact','Contact Ashutosh Trivedi at the University of Colorado Boulder.','<h1>Contact</h1>'+source_body('contact.md'))
# Keep the former group URL useful on hosts without redirect support.
page('/group/','Students / People','Students, postdoctoral researchers, and alumni of Ashutosh Trivedi.','<h1>Students / People</h1><p>The group page is now at <a href="/students/">Students / People</a>.</p>')
group=File.join(OUT,'group/index.html')
File.write(group,File.read(group).sub('<link rel="canonical" href="'+ORIGIN+'/group/">','<link rel="canonical" href="'+ORIGIN+'/students/">'))
FileUtils.cp(File.join(OUT,'assets/AshutoshTrivedi_CV.pdf'),File.join(OUT,'AshutoshTrivedi_CV.pdf'))
announcement=File.read(File.join(SRC,'open-positions/cardiac-digital-twin-rl-2026.html'))[/<body>(.*?)<\/body>/m,1].sub(/<h1>.*?<\/h1>/m,'')
page('/open-positions/cardiac-digital-twin-rl-2026.html','Spring 2026 research positions','Archived Spring 2026 student research announcement for cardiac digital twins and reinforcement learning.','<h1>Spring 2026 research positions</h1><p><strong>Archived announcement.</strong> This position announcement was posted in February 2026 for Spring 2026.</p>'+announcement)
Dir[File.join(SRC,'tags/*.md')].each do |f|
  data=YAML.load(File.read(f).split(/^---\s*$\n?/)[1])
  slug=File.basename(f,'.md'); tag=slug.downcase
  list=PAPERS.select{|p|p['tags'].any?{|t|t.downcase==tag}}
  path=data['permalink'] || '/tags/'+slug+'/'
  page(path,data['title'] || slug,'Publications by Ashutosh Trivedi in '+slug+'.','<h1>'+esc(data['title'] || slug)+'</h1><ol class="publications">'+list.map{|p|entry(p)}.join+'</ol>')
end
page('/tags/','Publication topics','Browse Ashutosh Trivedi’s publications by topic.','<h1>Publication topics</h1><ul>'+$routes.select{|p|p.start_with?('/tags/')}.map{|p|'<li><a href="'+p+'">'+esc(p.split('/')[-1])+'</a></li>'}.join+'</ul>')
page('/404.html','Page not found','The requested page could not be found.','<h1>Page not found</h1><p>Please visit the <a href="/">homepage</a> or browse <a href="/publications/">publications</a>.</p>')
File.write(File.join(OUT,'sitemap.xml'), '<?xml version="1.0" encoding="UTF-8"?>' + "\n" + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+$routes.reject{|p|['/404.html','/group/'].include?(p)}.map{|p|'<url><loc>'+ORIGIN+p+'</loc></url>'}.join+'</urlset>')
File.write(File.join(OUT,'robots.txt'),"User-agent: *\nAllow: /\nSitemap: #{ORIGIN}/sitemap.xml\n")
File.write(File.join(OUT,'.nojekyll'),'')
puts "Generated #{$routes.length} static HTML pages."
