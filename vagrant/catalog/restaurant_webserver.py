from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import cgi

engine=create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession=sessionmaker(bind=engine)
session=DBSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants=session.query(Restaurant).all()
                output=""
                output+="<html><body>"
                output+="<h1><a href='/restaurants/new'>Make a New Restaurant Here</a></h1>"
                for restaurant in restaurants:
                    output+="<h2>%s</h2>" % restaurant.name
                    output+="<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output+="</br>"
                    output+="<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
                output+="</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output=""
                output+="<html><body>"
                output+="<h1>Make a New Restaurant</h1>"
                output+="""
                <form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                <input name='newRestaurantName' type='text' placeholder='New Restaurant Name'>
                <input type='submit' value='Create'></form>
                """
                output+="</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                query = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output=""
                output+="<html><body>"
                output+="<h2>%s</h2>" % query.name
                output+="""
                <form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>
                <input name='newRestaurantName' type='text' placeholder='%s'>
                <input type='submit' value='Rename'></form>
                """ % (restaurantIDPath, query.name)
                output+="</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                query = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output=""
                output+="<html><body>"
                output+="<h1>Are you sure you want to delete %s?</h1>" % query.name
                output+="""
                <form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>
                <input type='submit' value='Delete'></form>
                """ % restaurantIDPath
                output+="</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent=fields.get('newRestaurantName')
                #Create new restaurant within database
                newRestaurant=Restaurant(name=messagecontent[0])
                session.add(newRestaurant)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent=fields.get('newRestaurantName')
                restaurantIDPath = self.path.split("/")[2]
                query = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                query.name = messagecontent[0]
                session.add(query)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                query = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                session.delete(query)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()

        except:
            pass
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
