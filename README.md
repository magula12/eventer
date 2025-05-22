# Eventer - Redmine Plugin

[English](#english) | [Slovak](#slovak)

## English

### Description
Eventer is a Redmine plugin that is mainly developed for management automation of employee assignments to issues, tasks, or events. It helps streamline the process of matching qualified team members with appropriate tasks based on their skills and availability.

### Requirements
- Redmine version: 6.0.2
- Ruby version: (included in Redmine image)
- Rails version: (included in Redmine image)
- Python version: 3.9
- PostgreSQL: latest

### Installation

#### Using Docker
1. Clone the repository:
```bash
git clone https://github.com/your-username/eventer.git
cd eventer
```

2. Build and run using Docker:
```bash
docker-compose up -d
```

#### Manual Installation
1. Copy the plugin directory to your Redmine plugins directory:
```bash
cp -r eventer /path/to/redmine/plugins/
```

2. Install dependencies:
```bash
cd /path/to/redmine
bundle install
```

3. Run database migrations:
```bash
bundle exec rake redmine:plugins:migrate RAILS_ENV=production
```

4. Restart your Redmine server

### Configuration
Before using the plugin, you need to set up the following in your Redmine instance:

1. Projects
   - Create and configure your project(s) where the plugin will be used

2. Roles
   - Define appropriate roles for users
   - Set up necessary permissions for each role

3. Users
   - Create user accounts for all team members
   - Assign appropriate roles to users

4. Issues
   - Configure issue types and workflows
   - Set up custom fields if needed

5. Issue Categories
    - Define Issue categories

6. User Qualifications
   - Define qualification categories
   - Assign qualifications to users
   - Set up qualification requirements for different types of tasks

### Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### License
This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

---

## Slovak

### Popis
Eventer je Redmine plugin, ktorý je primárne vyvíjaný pre automatizáciu manažmentu priradenia zamestnancov k problémom, úlohám alebo udalostiam. Pomáha zefektívniť proces priraďovania kvalifikovaných členov tímu k vhodným úlohám na základe ich zručností a dostupnosti.

### Požiadavky
- Redmine verzia: 6.0.2
- Ruby verzia: (obsiahnutá v Redmine image)
- Rails verzia: (obsiahnutá v Redmine image)
- Python verzia: 3.9
- PostgreSQL: latest

### Inštalácia

#### Použitie Dockeru
1. Naklonujte repozitár:
```bash
git clone https://github.com/your-username/eventer.git
cd eventer
```

2. Zostavte a spustite pomocou Dockeru:
```bash
docker-compose up -d
```

#### Manuálna inštalácia
1. Skopírujte adresár pluginu do adresára Redmine plugins:
```bash
cp -r eventer /cesta/k/redmine/plugins/
```

2. Nainštalujte závislosti:
```bash
cd /cesta/k/redmine
bundle install
```

3. Spustite databázové migrácie:
```bash
bundle exec rake redmine:plugins:migrate RAILS_ENV=production
```

4. Reštartujte váš Redmine server

### Konfigurácia
Pred použitím pluginu je potrebné nastaviť nasledujúce v inštancii Redmine:

1. Projekty
   - Vytvorte a nakonfigurujte svoje projekt(y), kde bude plugin používaný
   - Povoľte plugin pre konkrétne projekty

2. Role
   - Definujte vhodné role pre používateľov
   - Nastavte potrebné oprávnenia pre každú rolu

3. Používatelia
   - Vytvorte používateľské účty pre všetkých členov tímu
   - Priraďte vhodné role používateľom

4. Problémy (Issues)
   - Nakonfigurujte typy problémov a pracovné postupy
   - Nastavte vlastné polia podľa potreby

5. Kategórie probémov
   - Definujte kategórie problémov

6 Kvalifikácie používateľov
   - Definujte kategórie kvalifikácií
   - Priraďte kvalifikácie používateľom
   - Nastavte požiadavky na kvalifikácie pre rôzne typy úloh

### Prispievanie
1. Vytvorte fork repozitára
2. Vytvorte svoju feature vetvu (`git checkout -b feature/amazing-feature`)
3. Commitnite vaše zmeny (`git commit -m 'Add some amazing feature'`)
4. Pushnite do vetvy (`git push origin feature/amazing-feature`)
5. Otvorte Pull Request

### Licencia
Tento projekt je licencovaný pod GNU General Public License v3.0 - viac informácií nájdete v súbore LICENSE.