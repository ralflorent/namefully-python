from namefully import Name
from namefully.builder import NameBuilder

# Create a builder with initial names if any
builder = NameBuilder.of(Name.first('Nikola'), Name.last('Tesla'))

# Build the name
name = builder.build()
print(name)  # 'Nikola Tesla'

# Add a prefix
builder.add(Name.prefix('Mr'))

# Build the name with options if needed
name = builder.build(ordered_by='last_name', title='us')
print(name)  # 'Mr. Tesla Nikola'
