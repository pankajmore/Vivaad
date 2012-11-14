require 'nokogiri'
require 'open-uri'
require 'addressable/uri'
require 'csv'
require 'peach'

folder_path = "/home/pankajm/prog/Vivaad/data/Religion/controversial/"
output = "/home/pankajm/prog/Vivaad/data/Religion/c_religion_edit_history.csv"
def extracting_title(fname)
  File.basename(fname.chomp(File.extname(fname)), ".*")
end

files = Dir.glob(File.join(folder_path, "*"))

titles = files.map{|fname| File.basename(fname.chomp(File.extname(fname)), ".*") } 

def count_edit_history(title, count, continue=nil)
  url = Addressable::URI.parse("http://en.wikipedia.org/w/api.php")
  payload = {action: 'query', prop: 'revisions', rvprop: 'timestamp', rvlimit: 'max', titles: title, format: 'xml', export: 'exportnowrap', redirects: 'true' }

  payload[:rvcontinue] = continue unless continue.nil?

  url.query_values = payload
  #try catch open-uri
  begin
    doc = Nokogiri::XML(open(url.to_s))
  rescue StandardError=>e
    puts "Error fetching " + title + " with count " + count.to_s + "...retrying"
    sleep (1 + rand(3))
    retry
  else
    current_count = doc.css("revisions rev").length
    count += current_count
    if doc.css("query-continue revisions")[0] != nil
      cvalue = doc.css("query-continue revisions")[0].attributes['rvcontinue'].value
      return count_edit_history(title,count,cvalue)
    else
      return count
    end
  end
end

#results = titles.pmap(100) {|title| [title,count_edit_history(title,0)]} 

CSV.open(output, "w") do |csv|
  titles.peach(10) do |title|
    c = count_edit_history(title,0)
    puts title,c
    csv << [title, c]
  end
end
