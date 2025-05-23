const https = require('https');
const fs = require('fs');

function fetchJson(url) {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            let data = '';

            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    resolve(json);
                } catch (e) {
                    reject(e);
                }
            });
        }).on('error', reject);
    });
}

async function getVietnamData() {
    try {
        // Lấy danh sách tỉnh/thành phố
        const provinces = await fetchJson('https://provinces.open-api.vn/api/p/');

        // Duyệt từng tỉnh để lấy quận/huyện
        for (const province of provinces) {
            const provinceDetail = await fetchJson(`https://provinces.open-api.vn/api/p/${province.code}?depth=2`);
            province.districts = provinceDetail.districts;

            // Duyệt từng quận/huyện để lấy xã/phường
            for (const district of province.districts) {
                const districtDetail = await fetchJson(`https://provinces.open-api.vn/api/d/${district.code}?depth=2`);
                district.wards = districtDetail.wards;
            }
        }

        // Lưu dữ liệu ra file vietnam.json
        fs.writeFileSync('vietnam.json', JSON.stringify(provinces, null, 2), 'utf-8');
        console.log('Đã lưu dữ liệu vào file vietnam.json');
    } catch (error) {
        console.error('Lỗi khi lấy dữ liệu:', error);
    }
}

getVietnamData();
