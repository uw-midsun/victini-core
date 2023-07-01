set -e

mongosh <<EOF

use race-data

db.createCollection('car-location')

EOF
