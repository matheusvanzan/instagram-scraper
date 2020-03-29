import urllib.request
import os


class Profile:
    
    def __init__(self, username):
        self.username = username
        
        self.name = ''
        self.num_posts = 0
        self.num_followers = 0
        self.num_following = 0
        
        self.directory = 'data/' + username
        
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
            
        open('{}/posts.csv'.format(self.directory), 'w+')
            
    def __repr__(self):
        return '<Profile {}>'.format(self.username)
        
    def save(self):
        
        with open('{}/data.csv'.format(self.directory), 'w+') as f:
            
            f.write('"{}"; "{}"\n'.format('name',          self.name))
            f.write('"{}"; "{}"\n'.format('num_posts',     self.num_posts))
            f.write('"{}"; "{}"\n'.format('num_followers', self.num_followers))
            f.write('"{}"; "{}"\n'.format('num_following', self.num_following))
    
    
class Post:
    
    def __init__(self, profile):
        self.profile = profile
        self.id_ = 0
        self.url = ''
        
        self.lat = 0
        self.lng = 0
        self.desc = ''
        
    def __repr__(self):
        lenght = max(len(self.desc), 30)
        return '<Post {}: ({}, {}) {}...>'.format(
            self.id_, self.lat, self.lng, self.desc[:lenght])
        
    def download_img(self, src):
        filename = '{}/{}.png'.format(self.profile.directory, self.id_)
        urllib.request.urlretrieve(src, filename)
        
    def save(self):
        
        with open('{}/posts.csv'.format(self.profile.directory), 'a') as f:
            
            f.write('"{}"; "{}"; "{}"; "{}"\n'.format(
                self.id_, self.lat, self.lng, self.desc))